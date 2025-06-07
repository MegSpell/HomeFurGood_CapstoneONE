from flask import Flask, g, render_template, redirect, flash, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from models import db, User, SavedDog
from forms import SignUpForm, LoginForm
import requests
from petfinder_api import get_token, get_dogs

# ===========================
#        CONFIG CLASS
# ===========================
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")


# ===========================
#   APP & EXTENSION SETUP
# ===========================

# Initialize Flask extensions
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "login"  # Default redirect for @login_required
login_manager.login_message_category = "info"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # Add current user to global `g` so it's available in templates
    @app.before_request
    def add_user_to_global():
        g.user = current_user

    # Tell Flask-Login how to load a user from a user_id
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))  # Updated for SQLAlchemy 2.0
    # return User.query.get(int(user_id)) <------- deprecated: got this message when running tests so updated accordingly:  app.py:35: LegacyAPIWarning: The Query.get() method is considered legacy as of the 1.x series of SQLAlchemy and becomes a legacy construct in 2.0. The method is now available as Session.get() (deprecated since: 2.0) (Background on SQLAlchemy 2.0 at: https://sqlalche.me/e/b8d9)return User.query.get(int(user_id))

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)


# ===========================
#    TEMPORARY UTILITY ROUTES
# ===========================

@app.route("/init-db")
def init_db():
    """Temporary route to initialize database tables."""
    db.create_all()
    return "Database initialized!"



# ===========================
#       AUTH ROUTES
# ===========================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():  # If POST and form is valid
        user = User.register(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)  # Log the user in automatically
        flash(f"Account created! Welcome, {user.username}!", "success")
        return redirect("/")
    return render_template("auth/signup.html", form=form)  # Show form if GET or validation fails

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash(f"Welcome back, {user.username}!", "success")
            return redirect("/")
        else:
            flash("Invalid username or password.", "danger")
    return render_template("auth/login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect("/")


# ===========================
#       FAVORITES ROUTES
# ===========================

@app.route("/favorite", methods=["POST"])
@login_required
def favorite_dog():
    # Extract dog data from AJAX request JSON
    dog_id = request.json["dog_id"]
    dog_name = request.json["dog_name"]
    dog_photo = request.json.get("dog_photo", "")
    dog_url = request.json["dog_url"]

    # Check if this dog is already saved for the user
    existing = SavedDog.query.filter_by(user_id=current_user.id, dog_id=dog_id).first()
    if not existing:
        fav = SavedDog(
            user_id=current_user.id,
            dog_id=dog_id,
            dog_name=dog_name,
            dog_photo=dog_photo,
            dog_url=dog_url
        )
        db.session.add(fav)
        db.session.commit()
        return jsonify({"status": "added"})

    return jsonify({"status": "exists"})

@app.route("/unfavorite", methods=["POST"])
@login_required
def unfavorite_dog():
    dog_id = request.json["dog_id"]
    saved = SavedDog.query.filter_by(user_id=current_user.id, dog_id=dog_id).first()

    if saved:
        db.session.delete(saved)
        db.session.commit()
        return jsonify({"status": "removed"})

    return jsonify({"status": "not_found"})

@app.route("/favorites")
@login_required
def favorites_page():
    # Get all saved dogs for the current user
    favorites = SavedDog.query.filter_by(user_id=current_user.id).all()
    return render_template("favorites.html", favorites=favorites)


# ===========================
#       HOME ROUTES
# ===========================

@app.route("/")
def homepage():
    token = get_token()
    dogs = get_dogs(token, params={"limit": 3, "sort": "recent"})  # Spotlight dogs

    favorited_ids = {
        d.dog_id for d in SavedDog.query.filter_by(user_id=current_user.id).all()
    } if current_user.is_authenticated else set()

    return render_template("home.html", dogs=dogs, favorited_ids=favorited_ids)

# Fetch breed list from Petfinder API
def get_breeds(token):
    resp = requests.get(
        "https://api.petfinder.com/v2/types/dog/breeds",
        headers={"Authorization": f"Bearer {token}"}
    )
    resp.raise_for_status()
    data = resp.json()
    return [b["name"] for b in data["breeds"]]

@app.route("/search")
def search():
    token = get_token()
    clean_params = {"type": "dog", "limit": "100", "sort": "distance"}

    # Whitelist of valid query params to pass to Petfinder
    allowed_keys = [
        "location", "distance", "age", "gender", "size",
        "good_with_children", "good_with_dogs", "good_with_cats"
    ]

    for key in allowed_keys:
        if key == "breed":
            breeds = request.args.getlist("breed")
            breeds = [b for b in breeds if b]  # Remove blanks
            if breeds:
                clean_params["breed"] = breeds
        else:
            val = request.args.get(key)
            if val:
                clean_params[key] = val

    dogs = get_dogs(token, params=clean_params)

    favorited_ids = {
        d.dog_id for d in SavedDog.query.filter_by(user_id=current_user.id).all()
    } if current_user.is_authenticated else set()

    return render_template("search.html", dogs=dogs, favorited_ids=favorited_ids)

@app.route("/search-form")
def search_form():
    token = get_token()
    breeds = get_breeds(token)
    return render_template("search_form.html", breeds=breeds)

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

# Initialize SQLAlchemy and Bcrypt
db = SQLAlchemy()
bcrypt = Bcrypt()

######################################
#            USER MODEL
######################################

class User(UserMixin, db.Model):
    """User model for registered site users."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(20), unique=True, nullable=False)  # User's login name
    email = db.Column(db.String(50), unique=True, nullable=False)  # User's email
    password_hash = db.Column(db.String(100), nullable=False)  # Hashed password

    def __repr__(self):
        return f"<User #{self.id} {self.username}>"

    @classmethod
    def register(cls, username, email, password):
        """Register user with hashed password and return user instance."""
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        return cls(username=username, email=email, password_hash=hashed)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct."""
        user = cls.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            return user
        return False

######################################
#         SAVED DOG MODEL
######################################

class SavedDog(db.Model):
    """Dogs that users have saved/favorited."""

    __tablename__ = "saved_dogs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )  # Reference to the user who saved the dog

    dog_id = db.Column(db.String, nullable=False)       # Petfinder's unique dog ID
    dog_name = db.Column(db.String, nullable=False)     # Name of the dog
    dog_photo = db.Column(db.String)                    # URL to the dog's photo
    dog_url = db.Column(db.String)                      # Link to full dog listing

    # Prevent same dog from being saved multiple times by same user
    __table_args__ = (
        db.UniqueConstraint('user_id', 'dog_id'),
    )

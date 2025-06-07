from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

##########################################
#           SIGN-UP FORM
##########################################

class SignUpForm(FlaskForm):
    """Form for users to create an account."""

    username = StringField(
        "Username",
        validators=[
            InputRequired(),          # Field cannot be empty
            Length(min=3, max=20)     # Must be between 3 and 20 characters
        ]
    )

    email = StringField(
        "Email",
        validators=[
            InputRequired(),          # Field cannot be empty
            Email()                   # Must be a valid email address
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),          # Field cannot be empty
            Length(min=6)             # Minimum 6 characters for security
        ]
    )


##########################################
#            LOGIN FORM
##########################################

class LoginForm(FlaskForm):
    """Form for existing users to log in."""

    username = StringField(
        "Username",
        validators=[
            InputRequired()           # Must provide a username
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            InputRequired()           # Must provide a password
        ]
    )

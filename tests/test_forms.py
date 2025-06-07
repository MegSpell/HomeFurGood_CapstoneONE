from unittest import TestCase
from app import app
from forms import SignUpForm, LoginForm
from werkzeug.datastructures import MultiDict

class FormValidationTestCase(TestCase):
    """Tests for SignUpForm and LoginForm validation."""

    def setUp(self):
        """Disable CSRF for testing and set up test client."""
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()

    def test_valid_signup_form(self):
        """Form should validate with correct signup data."""
        with app.test_request_context():
            form = SignUpForm(formdata=MultiDict({
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }))
            self.assertTrue(form.validate())

    def test_invalid_signup_form_missing_fields(self):
        """Form should not validate if required fields are missing."""
        with app.test_request_context():
            form = SignUpForm(formdata=MultiDict({}))  # No data at all
            self.assertFalse(form.validate())

    def test_login_form_valid(self):
        """Login form should validate with correct data."""
        with app.test_request_context():
            form = LoginForm(formdata=MultiDict({
                "username": "testuser",
                "password": "password123"
            }))
            self.assertTrue(form.validate())

    def test_login_form_missing_username(self):
        """Login form should not validate if username is missing."""
        with app.test_request_context():
            form = LoginForm(formdata=MultiDict({
                "username": "",  # Missing username
                "password": "password123"
            }))
            self.assertFalse(form.validate())

    def test_login_form_missing_password(self):
        """Login form should not validate if password is missing."""
        with app.test_request_context():
            form = LoginForm(formdata=MultiDict({
                "username": "testuser",
                "password": ""  # Missing password
            }))
            self.assertFalse(form.validate())

import unittest
from app import app, db
from models import User
from flask_testing import TestCase

class AuthRouteTests(TestCase):
    """Test auth-related routes like signup, login, and logout."""

    def create_app(self):
        """Configure app for testing."""
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///home-fur-good-test"
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for test forms
        return app

    def setUp(self):
        """Set up test database and add one sample user."""
        db.create_all()

        # Create a sample user to use for login tests
        user = User.register(username="testuser", email="test@test.com", password="test123")
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean up database after each test."""
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        """Test user signup: form submission and success message."""
        with self.client:
            resp = self.client.post("/signup", data={
                "username": "newuser",
                "email": "new@example.com",
                "password": "newpass123"
            }, follow_redirects=True)

            # Expect a 200 OK and a success flash message
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Account created! Welcome, newuser!", resp.data)

    def test_login_valid(self):
        """Test logging in with valid credentials."""
        with self.client:
            resp = self.client.post("/login", data={
                "username": "testuser",
                "password": "test123"
            }, follow_redirects=True)

            # Expect a 200 OK and a welcome back message
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Welcome back, testuser!", resp.data)

    def test_login_invalid(self):
        """Test logging in with invalid credentials."""
        with self.client:
            resp = self.client.post("/login", data={
                "username": "testuser",
                "password": "wrongpass"
            }, follow_redirects=True)

            # Expect a 200 OK and an invalid login error message
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Invalid username or password.", resp.data)

    def test_logout(self):
        """Test logging out after logging in."""
        with self.client:
            # First log in the test user
            self.client.post("/login", data={
                "username": "testuser",
                "password": "test123"
            }, follow_redirects=True)

            # Then log out
            resp = self.client.get("/logout", follow_redirects=True)

            # Expect a 200 OK and a logout success message
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"You have been logged out.", resp.data)

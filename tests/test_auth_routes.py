import unittest
from app import app, db
from models import User
from flask_testing import TestCase

class AuthRouteTests(TestCase):
    """Test auth-related routes like signup, login, and logout."""

    def create_app(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///home-fur-good-test"
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

        user = User.register(username="testuser", email="test@test.com", password="test123")
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_signup(self):
        with self.client:
            resp = self.client.post("/signup", data={
                "username": "newuser",
                "email": "new@example.com",
                "password": "newpass123"
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Account created! Welcome, newuser!", resp.data)

    def test_login_valid(self):
        with self.client:
            resp = self.client.post("/login", data={
                "username": "testuser",
                "password": "test123"
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Welcome back, testuser!", resp.data)

    def test_login_invalid(self):
        with self.client:
            resp = self.client.post("/login", data={
                "username": "testuser",
                "password": "wrongpass"
            }, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Invalid username or password.", resp.data)

    def test_logout(self):
        with self.client:
            self.client.post("/login", data={
                "username": "testuser",
                "password": "test123"
            }, follow_redirects=True)

            resp = self.client.get("/logout", follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"You have been logged out.", resp.data)

import os
from unittest import TestCase
from app import app, db
from models import User, SavedDog
from flask import g

class HomeRoutesTestCase(TestCase):
    def setUp(self):
        """Set up test database and client with application context."""
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///home-fur-good-test"
            app.config["TESTING"] = True

            db.drop_all()
            db.create_all()

            user = User.register(
                username="testuser",
                email="test@example.com",
                password="test123"
            )
            db.session.add(user)
            db.session.commit()

            self.user = User.query.filter_by(username="testuser").first()

    def tearDown(self):
        """Clean up database after test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_homepage_logged_out(self):
        """Homepage should load for guests."""
        with self.client as client:
            resp = client.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Home Fur Good", resp.data)

    def test_homepage_logged_in(self):
        """Homepage should load for logged-in users."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess["_user_id"] = str(self.user.id)

            resp = client.get("/")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Home Fur Good", resp.data)

    def test_search_form_page(self):
        """Search form should render."""
        with self.client as client:
            resp = client.get("/search-form")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Zip Code", resp.data)

    def test_search_query(self):
        """Search query with minimal params should load."""
        with self.client as client:
            resp = client.get("/search?location=90210")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"dog-card", resp.data)  # Adjust as needed if template changes

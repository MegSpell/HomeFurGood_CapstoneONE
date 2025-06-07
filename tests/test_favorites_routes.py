import os
from unittest import TestCase
from app import app, db
from models import User, SavedDog

class FavoritesRoutesTestCase(TestCase):
    """Tests for favorites-related routes."""

    def setUp(self):
        """Create test client and add sample user inside app context."""
        self.app = app
        self.client = self.app.test_client()

        with self.app.app_context():
            app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///home-fur-good-test"
            app.config["TESTING"] = True

            db.drop_all()
            db.create_all()

            user = User.register(username="testuser", email="test@example.com", password="test123")
            db.session.add(user)
            db.session.commit()

            self.user_id = user.id

    def tearDown(self):
        """Clean up database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_favorite_dog(self):
        """Test adding a dog to favorites."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess["_user_id"] = str(self.user_id)

            resp = client.post("/favorite", json={
                "dog_id": "abc123",
                "dog_name": "Lucky",
                "dog_photo": "https://example.com/lucky.png",
                "dog_url": "https://www.petfinder.com/lucky"
            })

            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"added", resp.data)

    def test_unfavorite_dog(self):
        """Test removing a dog from favorites."""
        with self.app.app_context():
            fav = SavedDog(
                user_id=self.user_id,
                dog_id="xyz789",
                dog_name="Bella",
                dog_photo="https://example.com/bella.png",
                dog_url="https://www.petfinder.com/bella"
            )
            db.session.add(fav)
            db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess["_user_id"] = str(self.user_id)

            resp = client.post("/unfavorite", json={"dog_id": "xyz789"})
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"removed", resp.data)

    def test_favorites_page(self):
        """Test rendering the favorites page."""
        with self.app.app_context():
            fav = SavedDog(
                user_id=self.user_id,
                dog_id="abc123",
                dog_name="Lucky",
                dog_photo="https://example.com/lucky.png",
                dog_url="https://www.petfinder.com/lucky"
            )
            db.session.add(fav)
            db.session.commit()

        with self.client as client:
            with client.session_transaction() as sess:
                sess["_user_id"] = str(self.user_id)

            resp = client.get("/favorites")
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b"Lucky", resp.data)

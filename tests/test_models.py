import unittest
from app import create_app, db
from models import User, SavedDog

class UserModelTestCase(unittest.TestCase):
    """Test cases for User and SavedDog models."""

    def setUp(self):
        """Create test app and database."""
        self.app = create_app()
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///home-fur-good-test"
        self.app.config["TESTING"] = True

        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

            user1 = User.register("testuser1", "test1@example.com", "password1")
            user2 = User.register("testuser2", "test2@example.com", "password2")
            db.session.add_all([user1, user2])
            db.session.commit()

            self.user1_id = user1.id
            self.user2_id = user2.id

    def tearDown(self):
        """Tear down database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        """Test user registration stores correct data."""
        with self.app.app_context():
            user = User.query.get(self.user1_id)
            self.assertEqual(user.username, "testuser1")
            self.assertTrue(user.password_hash.startswith("$2b$"))

    def test_authenticate_valid(self):
        """Test valid login returns user."""
        with self.app.app_context():
            user = User.authenticate("testuser1", "password1")
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser1")

    def test_authenticate_invalid(self):
        """Test invalid login returns False."""
        with self.app.app_context():
            user = User.authenticate("testuser1", "wrongpass")
            self.assertFalse(user)

    def test_save_dog(self):
        """Test saving a dog to user's favorites."""
        with self.app.app_context():
            dog = SavedDog(
                user_id=self.user1_id,
                dog_id="dog123",
                dog_name="TestDog",
                dog_photo="https://example.com/dog.jpg",
                dog_url="https://example.com"
            )
            db.session.add(dog)
            db.session.commit()

            found = SavedDog.query.filter_by(user_id=self.user1_id).first()
            self.assertEqual(found.dog_name, "TestDog")

from app import app
from models import db, User, SavedDog

# Drop and recreate tables (optional for clean start)
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create regular users
    user1 = User.register(username="doglover1", email="dog1@example.com", password="woof123")
    user2 = User.register(username="puppyfan", email="puppy@example.com", password="bark456")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Add some fake saved dogs
    saved1 = SavedDog(
        user_id=user1.id, 
        dog_id="abc123", 
        dog_name="Puppy", 
        dog_photo="https://cdn-icons-png.flaticon.com/512/194/194279.png", 
        dog_url="https://www.petfinder.com")
    
    saved2 = SavedDog(
        user_id=user2.id, 
        dog_id="xyz789", 
        dog_name="Wuppy", 
        dog_photo="https://cdn-icons-png.flaticon.com/512/194/194279.png",
        dog_url="https://www.petfinder.com")

    db.session.add_all([saved1, saved2])
    db.session.commit()

    print("🌱 Seed data created!")

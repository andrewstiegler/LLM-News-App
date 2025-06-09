from backend.models import db, User  # adjust import path if needed
from sqlalchemy.exc import IntegrityError

def seed_user(user_id: str, email: str, name: str = None) -> User:
    """
    Check if user exists by user_id.
    If not, create and add user to DB.
    Returns the User instance.
    """
    print(f"👤 Seeding user: {user_id}")

    user = User.query.get(user_id)
    if user:
        # User already exists, just return it
        return user

    # Create new user
    new_user = User(id=user_id, email=email, name=name)
    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except IntegrityError:
        db.session.rollback()
        print("❌ Error committing user:", e)

        # If it fails due to a race condition or other, try to get the user again
        return User.query.get(user_id)

# migrations/fix_user_id.py

import os

from sqlalchemy import text

from app.database import SessionLocal
from app.models import ScheduledPost, User


def fix_scheduled_post_user_ids():
    db = SessionLocal()

    # SQLite-specific check for text user_ids
    db.execute(
        text(
            """
        UPDATE scheduled_posts
        SET user_id = 1
        WHERE typeof(user_id) = 'text'
    """
        )
    )

    db.commit()
    db.close()


def create_test_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        user = db.query(User).filter(User.id == 1).first()
        if user:
            print("Test user already exists")
            return

        # Create new user
        new_user = User(
            id=1,  # Using ID 1 to match the fix_scheduled_post_user_ids function
            username="testuser",
            email="test@example.com",
            hashed_password="password123",  # In a real app, hash this!
            api_key=os.environ.get("TWITTER_API_KEY"),
            api_secret=os.environ.get("TWITTER_API_SECRET"),
            access_token=os.environ.get("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
        )
        # App-only authentication
        bearer_token = os.environ.get("TWITTER_ACCESS_BEARER_TOKEN")

        # Choose auth method based on what you're doing
        # For v2 endpoints that don't need user context:
        # client = Client(bearer_token=bearer_token)

        # For user-context operations:
        # auth = tweepy.OAuthHandler(api_key, api_secret)
        # auth.set_access_token(access_token, access_token_secret)
        # api = tweepy.API(auth)

        db.add(new_user)
        db.commit()
        print("Test user created successfully")

    except Exception as e:
        db.rollback()
        print(f"Error creating test user: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    fix_scheduled_post_user_ids()
    print("Migration complete: Fixed string user_ids in scheduled_posts.")

    create_test_user()
    print("Migration complete: Created test user if needed.")

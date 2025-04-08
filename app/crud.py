from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def get_posts(db: Session):
    return db.query(models.ScheduledPost).all()


def create_post(db: Session, post: schemas.PostCreate):
    # Check if the user exists
    user = get_user(db, post.user_id)
    if not user:
        # use a default test user
        user_id = 1  # Default to test user
    else:
        user_id = post.user_id

    # Create a new ScheduledPost instance
    db_post = models.ScheduledPost(
        user_id=user_id,
        content=post.content,
        media_url=post.media_url,
        scheduled_time=post.scheduled_time,
        posted=False  # Set default value here
    )
    # Add the post to the database session
    db.add(db_post)
    # Commit the transaction to save the post
    db.commit()
    # Refresh the instance to get the updated data from the database (like the id)
    db.refresh(db_post)
    # Return the created post
    return db_post


def get_scheduled_post_by_id(db, post_id):
    """
    Retrieves a specific scheduled post by its ID.

    Args:
        db: Database session
        post_id: ID of the post to retrieve

    Returns:
        The scheduled post object or None if not found
    """
    return db.query(models.ScheduledPost).filter(models.ScheduledPost.id == post_id).first()


def get_due_scheduled_posts(db, current_time):
    """
    Retrieves all posts that are scheduled to be published at or before the current time
    and have not been published yet.

    Args:
        db: Database session
        current_time: Current datetime to check against

    Returns:
        List of scheduled post objects that are due for publishing
    """
    return db.query(models.ScheduledPost).filter(
        models.ScheduledPost.scheduled_time <= current_time,
        models.ScheduledPost.posted == False
    ).all()


def get_user(db, user_id):
    """
    Retrieves a user by ID.

    Args:
        db: Database session
        user_id: ID of the user to retrieve

    Returns:
        The user object or None if not found
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

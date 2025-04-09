import celery
import tweepy
import logging
from datetime import datetime
from . import crud, database
from celery import Celery

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_twitter_api(api_key, api_secret, access_token, access_token_secret):
    """
    Create and return a tweepy API object with the provided credentials.
    """
    auth = tweepy.OAuth1UserHandler(
        api_key, api_secret, access_token, access_token_secret
    )
    return tweepy.API(auth)


# Initialize Celery
celery_app = Celery("x_content_scheduler")
# You'd also need to configure Celery with Redis/RabbitMQ here
celery_app.conf.broker_url = "redis://redis:6379/0"  # or whatever broker you're using


# Your existing function with Celery decorator
@celery_app.task
def post_scheduled_content(post_id=None) -> bool:
    """
    Function to post scheduled content to X (Twitter).

    Args:
        post_id (int, optional): ID of a specific post to publish.
                                 If None, processes all due posts.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        with database.SessionLocal() as db:
            current_time = datetime.now()

            if post_id:
                post = crud.get_scheduled_post_by_id(db, post_id)
                if not post:
                    logger.error(f"No post found with ID {post_id}")
                    return False
                posts = [post]
            else:
                posts = crud.get_due_scheduled_posts(db, current_time)
                if not posts:
                    logger.info("No posts scheduled for publishing at this time")
                    return True

            for post in posts:
                user = crud.get_user(db, post.user_id)
                if not user:
                    logger.error(f"No user found with ID {post.user_id}")
                    continue  # Skip to next post

                try:
                    api = get_twitter_api(
                        user.api_key,
                        user.api_secret,
                        user.access_token,
                        user.access_token_secret,
                    )
                    api.update_status(post.content)
                    post.posted = True
                    db.commit()
                    logger.info(f"Post with ID {post.id} published successfully.")
                except Exception as post_err:
                    logger.error(f"Failed to post content ID {post.id}: {post_err}")
                    continue  # Log and skip to the next

        return True

    except Exception as e:
        logger.error(f"An error occurred in post_scheduled_content: {e}")
        return False

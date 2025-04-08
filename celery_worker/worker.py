from app.tasks import celery_app

celery_app.worker_main(["worker", "--loglevel=info"])

# This code is used to run the Celery worker for the FastAPI application.
# It imports the Celery instance from the tasks module and starts the worker with the specified log level.
# The worker will listen for tasks and execute them as they are received.
# The worker will process tasks in the background, allowing the FastAPI application to remain responsive to incoming requests.
# This is useful for handling long-running tasks, such as posting scheduled content to X (Twitter).
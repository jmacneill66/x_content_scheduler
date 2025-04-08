# X Content Scheduler

A content scheduling system for X (formerly Twitter), allowing users to draft, schedule, and publish posts with media attachments. This system utilizes FastAPI (Python) on the backend, React (JavaScript) for the frontend, and a Celery + Redis-based queue system for scheduling and publishing tasks. For manual testing, Swagger UI has been included.

## Features

- **Drafting Interface**: Allows users to create posts with text input, media attachments, and tag suggestions.
- **Scheduling Engine**: Set a future date/time for publishing posts. Includes timezone support.
- **Post Preview**: Users can preview their posts on a timeline, with both mobile and desktop views.
- **Publishing Mechanism**: Automatically posts content at the scheduled time, handles rate limits and retries.
- **Database**: Stores drafts and scheduled posts in SQLite; persistent volume through docker file.
- **Queue System**: Celery + Redis (or RQ) for handling timed background tasks.
- **OAuth Authentication**: Users authenticate via OAuth, and their credentials are securely stored for future post publishing.
- **Future implementation: PostgreSQL could be deployed with Amazon CDN.

## Tech Stack

- **Backend**: Python (FastAPI)
- **Queue System**: Celery + Redis
- **Frontend**: React.js (for the content drafting and preview interface)
- **Database**: SQLite
- **Authentication**: OAuth 2.0 for X authentication
- **Task Queue**: Celery for managing background tasks (scheduled posts)

## Frontend Flow

1. Users authenticate via OAuth with X (currently a simulated local environment).
2. Users can draft posts with text input, media attachments, and tags.
3. The user can preview how the post will look on their X timeline (both mobile and desktop).
4. The user schedules the post to be published at a specified date and time.
5. Celery workers run asynchronously to post content at the scheduled time.

## Environment Setup

This project requires several API credentials from X (Twitter) to function properly:

1. Create a developer account at [X Developer Portal](https://developer.twitter.com/)
2. Create a new project and app to get your credentials
3. Create a `.env` file in the project root with the following variables:

```bash
DATABASE_URL=sqlite:///app.db
CELERY_BROKER_URL=redis://redis:6379/0

TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
```

## Setup Instructions

### Prerequisites

- **Docker** and **Docker Compose** installed.
- **Node.js** and **npm/yarn** for the React frontend.

### Step-by-step Setup

1. **Start Redis**:

   ```bash
   docker-compose up -d redis
   ```

2. **Start the Celery Worker**:

   ```bash
   PYTHONPATH=. python -m celery_worker.worker
   ```

3. **Start the FastAPI Application**:

   ```bash
   # Run the entire stack using Docker Compose
   docker-compose up
   
   # Or to run in the background
   docker-compose up -d

### Frontend Setup (React)

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Start the frontend development server:

   ```bash
   npm start
   ```

### Backend Setup (FastAPI)

1. **Create a `.env` file** for database and API configurations:

   ```bash
   DATABASE_URL=sqlite:///./app.db
   CELERY_BROKER_URL=redis://redis:6379/0
   ```

2. **Configure credentials in `app/migrations/fix_user_id.py`**.

3. **Migrate the database**:

   ```bash
   alembic upgrade head
   ```

4. **Run FastAPI**:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

Open Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

## Docker Setup

This project uses Docker Compose to manage multiple services. It includes:

- **FastAPI** backend service.
- **Redis** for background task queue.
- **Celery worker** to process scheduled tasks.

The `docker-compose.yml` file includes everything you need to get the project up and running.

```bash
docker-compose up --build
```

To stop services:

```bash
docker-compose down
```

## Authentication with X (formerly Twitter)

OAuth flow with token validation and scheduled task execution using **Tweepy**.

## Known Limitations and Features in Progress

- React frontend is WIP; UX/UI improvements planned.
- Retry mechanism and rate-limit handling to be enhanced.

## Contribution Guidelines

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a Pull Request.

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Directory Structure

```bash
.
x_content_scheduler/
├── Dockerfile
├── README.md
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── migrations/
│   │   └── workflows/
│   │       ├── ci.yml
│   │       └── cd.yml
│   ├── models.py
│   ├── schemas.py
│   └── tasks.py
├── app.db
├── celery_worker/
│   └── worker.py
├── docker-compose.test.yml
├── docker-compose.yml
├── requirements.txt
├── tests/
│   └── test_api.py

```

---

Author: <jeffrey.macneill@gmail.com>  
GitHub: [jmacneill66](https://github.com/jmacneill66)  
X: [@JMACNEILL66](https://x.com/JMACNEILL66)

---

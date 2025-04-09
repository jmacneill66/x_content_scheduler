# tests/test_api.py
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_scheduled_post():
    response = client.post(
        "/schedule/",
        json={
            "user_id": 1,
            "content": "Test scheduled post",
            "scheduled_time": (datetime.now() + timedelta(hours=1)).isoformat(),
            "media_url": None,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Test scheduled post"
    assert data["user_id"] == 1

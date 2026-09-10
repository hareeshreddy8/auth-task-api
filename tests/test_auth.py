from fastapi.testclient import TestClient
import os
os.environ["Testing"] = "Testing"

if os.path.exists("test.db"):
    os.remove("test.db")

from api import auth_app

client = TestClient(auth_app)

import pytest

@pytest.fixture
def auth_token():
    signup = client.post(
        "/signup",
        params={
            "username": "harees",
            "password": "abc12344"
        }
    )

    login = client.post(
        "/login",
        params={
            "username": "harees",
            "password": "abc12344"
        }
    )

    return login.json()["access_token"]
def test_insert_task(auth_token):

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    request = client.post(
        "/tasks",
        json={
            "name": "project1",
            "priority": "high",
            "due_date": "2026-09-10"
        },
        headers=headers
    )

    print(request.json())

    assert request.status_code == 200
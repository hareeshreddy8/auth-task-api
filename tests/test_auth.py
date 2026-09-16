from fastapi.testclient import TestClient
import os
import pytest
import database

@pytest.fixture
def reset_db():
    os.environ["Testing"] = "Testing"

    if os.path.exists("test.db"):
        os.remove("test.db")

    database.create_table_users()
    database.create_table_tasks()

from api import auth_app

client = TestClient(auth_app)


@pytest.fixture
def auth_token(reset_db):
    signup = client.post(
        "/signup",
        params={
            "username": "test",
            "password": "abc12344"
        }
    )
    assert signup.status_code == 201
    login = client.post(
        "/login",
        params={
            "username": "test",
            "password": "abc12344"
        }
    )

    assert login.status_code == 200
    return login.json()["access_token"]


@pytest.fixture
def task(auth_token):

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

    assert request.status_code == 200
    print(request.json())
    return request.json()



def test_delete_task(auth_token, task):
    task_id = task["data"]["id"]

    request = client.delete(
        f"/tasks/{task_id}",
        headers= {
        "Authorization": f"Bearer {auth_token}"
    }
    )
    assert request.status_code == 204

def test_complete_task(auth_token, task):
    task_id = task["data"]["id"]

    header = {
        "Authorization" : f"Bearer {auth_token}"
    }

    request = client.patch(
        f"/tasks/{task_id}/complete",
        headers=header
    )
    assert request.status_code == 200



def test_get_tasks(auth_token, task):

    second_task = client.post(
        "/tasks",
        headers=
        {
            "Authorization": f"Bearer {auth_token}"
        },
        json={
            "name": "project2",
            "priority": "low",
            "due_date": "2026-09-10"
        }
    )
    request = client.get(
        "/tasks",
        headers=
        {
            "Authorization" : f"Bearer {auth_token}"
        },
        params=
        {
            "limit":1,
            "offset":1
        }
    )

    assert request.status_code == 200
    assert request.json()["count"] == 2
    assert request.json()["data"][0]["id"] == second_task.json()["data"]["id"]


def test_filter_tasks_by_priority(auth_token,task):

    second_task = client.post(
            "/tasks",
            headers=
            {
                "Authorization": f"Bearer {auth_token}"
            },
            json={
                "name": "project2",
                "priority": "low",
                "due_date": "2026-09-10"
            }
        )
    
    header = {
        "Authorization" : f"Bearer {auth_token}"
    }

    request = client.request(
        "GET",
        "/tasks/filter",
        headers= {
        "Authorization" : f"Bearer {auth_token}"
    },
        params={
            "priority" : "low"
        }
    )

    assert request.status_code == 200
    print(request.json())


def test_filter_tasks_by_status(auth_token,task):

    client.post(
            "/tasks",
            headers=
            {
                "Authorization": f"Bearer {auth_token}"
            },
            json={
                "name": "project2",
                "priority": "low",
                "due_date": "2026-09-10"
            }
        )
    task_id = task["data"]["id"]
    complete_task = client.patch(
        f"/tasks/{task_id}/complete",
        headers={
            "Authorization": f"Bearer {auth_token}"
        }
    )


    request = client.request(
        "GET",
        "/tasks/filter",
        headers= {
        "Authorization" : f"Bearer {auth_token}"
    },
        params={
            "status":True
        }
    )

    assert request.status_code == 200
    assert request.json()["data"][0]["id"] == task_id
    print("status",request.json())


def test_sort_tasks(auth_token,task):
    client.post(
            "/tasks",
            headers=
            {
                "Authorization": f"Bearer {auth_token}"
            },
            json={
                "name": "project2",
                "priority": "low",
                "due_date": "2026-09-10"
            }
        )

    task_id = task["data"]["id"]

    request = client.get(
        "/tasks/sort",
        params={
            "by":"priority"
        },
        headers={
            "Authorization":f"Bearer {auth_token}"
        }
    )
    assert request.status_code == 200
    print(request.json())
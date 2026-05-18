import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import storage

@pytest.fixture
def client():
    storage.clear()
    return TestClient(app)

def test_create_task(client):
    response = client.post("/tasks", json={
        "title": "Test task",
        "description": "Desc",
        "status": "todo",
        "priority": 3
    }, headers={"X-User-Id": "10"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"

def test_create_task_short_title(client):
    response = client.post("/tasks", json={
        "title": "ab",
        "description": "Desc",
        "status": "todo",
        "priority": 3
    }, headers={"X-User-Id": "10"})
    assert response.status_code == 422

def test_create_task_no_auth(client):
    response = client.post("/tasks", json={
        "title": "Task",
        "status": "todo",
        "priority": 3
    })
    assert response.status_code == 401

def test_user_sees_only_own_tasks(client):
    client.post("/tasks", json={"title": "User10 task", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    client.post("/tasks", json={"title": "User20 task", "status": "todo", "priority": 3}, headers={"X-User-Id": "20"})
    response = client.get("/tasks", headers={"X-User-Id": "10"})
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "User10 task"

def test_filter_tasks(client):
    client.post("/tasks", json={"title": "Low priority", "status": "todo", "priority": 2}, headers={"X-User-Id": "10"})
    client.post("/tasks", json={"title": "High priority", "status": "in_progress", "priority": 4}, headers={"X-User-Id": "10"})
    response = client.get("/tasks?min_priority=3", headers={"X-User-Id": "10"})
    assert len(response.json()) == 1
    assert response.json()[0]["priority"] >= 3

def test_update_status(client):
    resp = client.post("/tasks", json={"title": "Task", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    task_id = resp.json()["id"]
    response = client.patch(f"/tasks/{task_id}/status", json={"status": "done"}, headers={"X-User-Id": "10"})
    assert response.status_code == 200
    assert response.json()["status"] == "done"

def test_access_foreign_task(client):
    resp = client.post("/tasks", json={"title": "Task", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    task_id = resp.json()["id"]
    response = client.get(f"/tasks/{task_id}", headers={"X-User-Id": "99"})
    assert response.status_code == 404

def test_delete_task(client):
    resp = client.post("/tasks", json={"title": "Task", "status": "todo", "priority": 3}, headers={"X-User-Id": "10"})
    task_id = resp.json()["id"]
    response = client.delete(f"/tasks/{task_id}", headers={"X-User-Id": "10"})
    assert response.status_code == 204
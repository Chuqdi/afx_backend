from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message`": "Hello World!"}


def test_read_users():
    user_id = 1
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User details retrieved", "user_id": user_id}

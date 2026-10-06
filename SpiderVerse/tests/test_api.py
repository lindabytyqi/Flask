from tests.conftest import login


def test_public_get_characters(client):
    response = client.get("/api/characters")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Spider"


def test_anonymous_cannot_create_universe(client):
    response = client.post("/api/universes", json={
        "name": "New Universe",
        "description": "Test",
        "image": "test.jpg",
        "actor": "Actor",
    })
    assert response.status_code == 401


def test_normal_user_cannot_create_universe(client):
    login(client, "user@test.local", "User123!")
    response = client.post("/api/universes", json={
        "name": "New Universe",
        "description": "Test",
        "image": "test.jpg",
        "actor": "Actor",
    })
    assert response.status_code == 403


def test_admin_can_create_universe(client):
    login(client, "admin@test.local", "Admin123!")
    response = client.post("/api/universes", json={
        "name": "New Universe",
        "description": "Test",
        "image": "test.jpg",
        "actor": "Actor",
    })
    assert response.status_code == 201
    assert response.get_json()["name"] == "New Universe"


def test_search(client):
    response = client.get("/api/search?q=Spider")
    assert response.status_code == 200
    assert response.get_json()[0]["name"] == "Test Spider"

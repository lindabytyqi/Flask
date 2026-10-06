from tests.conftest import login


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"SPIDER" in response.data


def test_movies_page(client):
    response = client.get("/movies/")
    assert response.status_code == 200
    assert b"Test Movie" in response.data


def test_character_detail(client):
    response = client.get("/characters/1")
    assert response.status_code == 200
    assert b"Test Spider" in response.data


def test_admin_redirects_when_anonymous(client):
    response = client.get("/admin/")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_normal_user_cannot_open_admin(client):
    login(client, "user@test.local", "User123!")
    response = client.get("/admin/")
    assert response.status_code == 403


def test_admin_can_open_admin(client):
    login(client, "admin@test.local", "Admin123!")
    response = client.get("/admin/")
    assert response.status_code == 200
    assert b"Dashboard" in response.data

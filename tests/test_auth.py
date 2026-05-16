import uuid
import pytest

from httpx import (
    AsyncClient,
    ASGITransport
)

from app.main import app


@pytest.mark.asyncio
async def test_register():

    transport = ASGITransport(app=app)

    unique_id = str(uuid.uuid4())

    email = f"{unique_id}@test.com"
    username = f"user_{unique_id[:8]}"

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.post(
            "/register",
            json={
                "username": username,
                "email": email,
                "password": "123456"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == email


@pytest.mark.asyncio
async def test_login():

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        response = await ac.post(
            "/login",
            data={
                "username": "test@test.com",
                "password": "123456"
            }
        )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_protected_route():

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        login_response = await ac.post(
            "/login",
            data={
                "username": "test@test.com",
                "password": "123456"
            }
        )

        login_data = login_response.json()

        token = login_data["access_token"]

        response = await ac.get(
            "/protected",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_refresh_token():

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        login_response = await ac.post(
            "/login",
            data={
                "username": "test@test.com",
                "password": "123456"
            }
        )

        login_data = login_response.json()

        refresh_token = login_data[
            "refresh_token"
        ]

        response = await ac.post(
            f"/refresh?refresh_token={refresh_token}"
        )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data


@pytest.mark.asyncio
async def test_logout_and_blacklist():

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:

        login_response = await ac.post(
            "/login",
            data={
                "username": "test@test.com",
                "password": "123456"
            }
        )

        login_data = login_response.json()

        token = login_data[
            "access_token"
        ]

        logout_response = await ac.post(
            "/logout",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

        assert logout_response.status_code == 200

        protected_response = await ac.get(
            "/protected",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    assert protected_response.status_code == 401
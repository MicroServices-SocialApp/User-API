# test_user.py

from httpx import AsyncClient
import pytest


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/user/create",
        json={"username": "string", "email": "string", "password": "string"},
    )
    print(response)
    assert response.status_code == 201

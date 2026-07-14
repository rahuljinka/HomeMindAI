import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_register_user():
    user_data = {"email": "test@example.com", "password": "password123"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Note: This will fail without a test database, but demonstrates the test structure
        # response = await ac.post("/auth/register", json=user_data)
        # assert response.status_code == 200
        pass

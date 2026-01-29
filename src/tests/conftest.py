import httpx
import pytest
from httpx import ASGITransport

from app.main import app

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
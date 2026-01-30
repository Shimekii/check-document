import httpx
import pytest
from httpx import ASGITransport
from tests.mocks.FakeRedis import FakeRedis
from app.dependencies.redis import get_redis
from app.main import app

@pytest.fixture
async def fake_redis():
    redis = FakeRedis()
    yield redis


@pytest.fixture
async def async_client(fake_redis):
    app.dependency_overrides[get_redis] = lambda: fake_redis
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url='http://test') as client:
        yield client
import pytest

from instagram_service.main import main as main_func

@pytest.mark.asyncio
async def test_main():
    assert await main_func()

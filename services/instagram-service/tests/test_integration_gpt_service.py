import os
import pytest

from instagram_service.services import GptService
from instagram_service.services import AppConfig

@pytest.fixture
def gpt_fixture():
    config = AppConfig(os.environ)
    gpt_service = GptService(config)
    return gpt_service

@pytest.mark.asyncio
async def test_ask(gpt_fixture):
     await gpt_fixture.ask(os.environ.get('TEST_QUERY'))

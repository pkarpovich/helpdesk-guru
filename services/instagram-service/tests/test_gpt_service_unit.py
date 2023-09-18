import os
import pytest

from instagram_service.services import (
    GptService,
    AppConfig,
)


@pytest.fixture
def gpt_fixture():
    config = AppConfig(os.environ)
    gpt_service = GptService(config)
    return gpt_service

@pytest.mark.asyncio
async def test_ask(gpt_fixture,mocker):
    mocker.patch.object(gpt_fixture,'ask',return_value=str)
    assert await gpt_fixture.ask(os.environ.get('TEST_QUERY')) == str


import pytest
from grpclib.client import Channel

from instagram_service.services import GptService, AppConfig, InstagramService
from lib.gpt import GptServiceStub


@pytest.fixture
def mock_gpt_service(mocker):
    app_config = mocker.MagicMock(spec=AppConfig)
    return GptService(app_config)

@pytest.fixture
def mock_gpt_stub(mocker):
    channel = mocker.MagicMock(spec=Channel)
    return GptServiceStub(channel)

@pytest.fixture
def mock_instagram_service(mocker):
    app_config = mocker.MagicMock(spec=AppConfig)
    return InstagramService(app_config)
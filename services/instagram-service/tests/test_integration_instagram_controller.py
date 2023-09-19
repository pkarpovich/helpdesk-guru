import pytest
import os

from instagram_service.services import (
    GptService,
    InstagramService,
    AppConfig
)

from instagram_service.controller import InstagramContoller


@pytest.fixture
def instagram_controller_fixture1():
    config = AppConfig(os.environ)

    gpt_service = GptService(config)
    instagram_service = InstagramService(config)

    instagram_controller = InstagramContoller()
    instagram_controller.__int__(instagram_service,gpt_service)

    return instagram_controller
    
@pytest.fixture
def instagram_controller_fixture2():
    config = AppConfig(os.environ)

    gpt_service = GptService(config)
    instagram_service = InstagramService(config)

    instagram_controller = InstagramContoller()
    instagram_controller.__int__(instagram_service,gpt_service)
    
    instagram_controller.login()

    return instagram_controller

def test_login(instagram_controller_fixture1):
    assert instagram_controller_fixture1.login()

def test_read(instagram_controller_fixture2):
    assert instagram_controller_fixture2.read_direct_messages()

@pytest.mark.asyncio
async def test_ask(instagram_controller_fixture1):
    assert await instagram_controller_fixture1.ask(os.environ.get('QUERY'))

def test_send(instagram_controller_fixture2):
    assert isinstance(os.environ.get('TEST_MESSAGE'),str)
    assert isinstance(os.environ.get('TEST_SENDER_USERNAME'),str)
    
    assert instagram_controller_fixture2.send_direct_messages(os.environ.get('TEST_MESSAGE'), os.environ.get('TEST_SENDER_USERNAME'))

@pytest.mark.asyncio
async def test_start(instagram_controller_fixture1):
    assert await instagram_controller_fixture1.start()

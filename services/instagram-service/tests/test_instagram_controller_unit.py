import pytest
import os

from instagram_service.services import (
    GptService,
    InstagramService,
    AppConfig
)

from instagram_service.controller import InstagramContoller


@pytest.fixture
def instagram_controller_fixture():
    config = AppConfig(os.environ)

    gpt_service = GptService(config)
    instagram_service = InstagramService(config)

    instagram_controller = InstagramContoller()
    instagram_controller.__int__(instagram_service,gpt_service)

    return instagram_controller

def test_login(instagram_controller_fixture,mocker):
    mocker.patch.object(instagram_controller_fixture,'login',return_value=None)
    assert instagram_controller_fixture.login() == None

def test_read(instagram_controller_fixture,mocker):
    mocker.patch.object(instagram_controller_fixture, 'login', return_value=None)
    assert instagram_controller_fixture.login() == None

    mocker.patch.object(instagram_controller_fixture,'read_direct_messages',return_value=list)
    assert instagram_controller_fixture.read_direct_messages() == list

@pytest.mark.asyncio
async def test_ask(instagram_controller_fixture,mocker):
    mocker.patch.object(instagram_controller_fixture,'ask',return_value=str)
    assert await instagram_controller_fixture.ask(os.environ.get('QUERY')) == str

def test_send(instagram_controller_fixture,mocker):
    mocker.patch.object(instagram_controller_fixture, 'login', return_value=None)
    assert instagram_controller_fixture.login() == None

    mocker.patch.object(instagram_controller_fixture,'send_direct_messages',return_value=None)
    assert isinstance(os.environ.get('TEST_MESSAGE'),str)
    assert isinstance(os.environ.get('TEST_SENDER_USERNAME'),str)
    assert instagram_controller_fixture.send_direct_messages(os.environ.get('TEST_MESSAGE'), os.environ.get('TEST_SENDER_USERNAME')) == None

@pytest.mark.asyncio
async def test_start(instagram_controller_fixture,mocker):
    mocker.patch.object(instagram_controller_fixture,'start',return_value=None)
    assert await instagram_controller_fixture.start() == None

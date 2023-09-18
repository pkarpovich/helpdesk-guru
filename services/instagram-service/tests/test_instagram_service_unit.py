import os
import pytest

from instagram_service.services import (
    AppConfig,
    InstagramService,
)


@pytest.fixture
def fix_ture():
    config=AppConfig(os.environ)
    instagram_service=InstagramService(config)

    return instagram_service

def test_login_read(fix_ture,mocker):
    mocker.patch.object(fix_ture, 'login', return_value=None)
    assert fix_ture.login() == None

    mocker.patch.object(fix_ture, 'read_direct_messages', return_value=list)
    assert fix_ture.read_direct_messages() == list

def test_login_send(fix_ture,mocker):
    mocker.patch.object(fix_ture, 'login', return_value=None)
    assert fix_ture.login() == None

    mocker.patch.object(fix_ture,'send_direct_message',return_value=None)

    assert isinstance(os.environ.get('TEST_MESSAGE'),str)
    assert isinstance(os.environ.get('TEST_SENDER_USERNAME'),str)
    assert fix_ture.send_direct_message(os.environ.get('TEST_MESSAGE'), os.environ.get('TEST_SENDER_USERNAME')) == None

def test_login(mocker, fix_ture):
    mocker.patch.object(fix_ture, 'login', return_value=None)
    assert fix_ture.login() == None

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
    instagram_service.login()

    return instagram_service

def test_read(fix_ture):
   assert fix_ture.read_direct_messages()
   messages = fix_ture.read_direct_messages()
   assert isinstance(messages, list)

def test_send(fix_ture):
    assert isinstance(os.environ.get('TEST_MESSAGE'),str)
    assert isinstance(os.environ.get('TEST_SENDER_USERNAME'),str)
    assert fix_ture.send_direct_message(os.environ.get('TEST_MESSAGE'), os.environ.get('TEST_SENDER_USERNAME'))
    result = fix_ture.send_direct_message(os.environ.get('TEST_MESSAGE'), os.environ.get('TEST_SENDER_USERNAME'))
    assert result is None

#!/usr/bin/env python3
import pytest
from server.resources.utils import Serializer

@pytest.mark.incremental
def test_serializer(mock_user):
    token = Serializer.generate_token(**mock_user)
    assert token, "should return new token"
    assert Serializer.confirm_token(token) == mock_user['email'], "should be confirmable by token owner"
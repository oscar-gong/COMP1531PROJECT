'''This module tests channel invite'''
import pytest
from channel import channel_invite
from channels import channels_create
from error import InputError, AccessError
from projectDefines import user1, user2, user3
from pytestHelperFunctions import create_login_user
from database import database

def test_valid_channel():
    '''Tests valid channel'''
    database.reset()

    test_user1 = create_login_user(user1)
    test_user2 = create_login_user(user2)
    test_channel = channels_create(test_user2["token"], "Test Channel 1", True)
    assert channel_invite(test_user2["token"], test_channel["channel_id"], test_user1["u_id"]) == {}
    owner = database.get_user_object(test_user1['token'])
    channel = database.get_channel_by_id(test_channel['channel_id'])
    assert channel.is_owner(owner)

def test_invalid_channel_id():
    '''Tests invalid channel id'''
    database.reset()
    test_user1 = create_login_user(user1)
    test_user2 = create_login_user(user2)
    with pytest.raises(InputError):
        channel_invite(test_user1["token"], 5555555, test_user2["u_id"])

def test_invalid_user_id():
    '''Tests invalid user id'''
    database.reset()
    test_user1 = create_login_user(user1)
    test_channel = channels_create(test_user1["token"], "Test Channel 1", True)
    with pytest.raises(InputError):
        channel_invite(test_user1["token"], test_channel["channel_id"], 5555555)

def test_user_not_in_channel():
    '''Tests when user is not in channel'''
    database.reset()
    test_user1 = create_login_user(user1)
    test_user2 = create_login_user(user2)
    test_user3 = create_login_user(user3)
    test_channel = channels_create(test_user1["token"], "Test Channel 1", True)
    with pytest.raises(AccessError):
        channel_invite(test_user2["token"], test_channel["channel_id"], test_user3["u_id"])

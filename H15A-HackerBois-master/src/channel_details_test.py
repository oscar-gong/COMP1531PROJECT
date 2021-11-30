'''This module tests channel details'''
import pytest
from channel import channel_invite, channel_details
from channels import channels_create
from error import InputError, AccessError
from projectDefines import user1, user2, user3
from pytestHelperFunctions import create_login_user, change_to_member
from database import database

def test_valid_channel_with_1_user():
    '''Tests valid channel with one user'''
    database.reset()
    test_user1 = create_login_user(user1)
    test_channel = channels_create(test_user1["token"], "Hayden", True)
    expected = {
        "name" : "Hayden",
        "owner_members" : [change_to_member(test_user1)],
        "all_members" : [change_to_member(test_user1)]
    }
    assert channel_details(test_user1["token"], test_channel["channel_id"]) == expected

def test_valid_channel_with_multiple_users():
    '''Tests valid channel with multiple users'''
    database.reset()
    test_user1 = create_login_user(user1)
    test_user2 = create_login_user(user2)
    test_user3 = create_login_user(user3)
    test_channel = channels_create(test_user1["token"], "My Channel", True)
    channel_invite(test_user1["token"], test_channel["channel_id"], test_user2["u_id"])
    channel_invite(test_user1["token"], test_channel["channel_id"], test_user3["u_id"])
    expected = {
        "name" : "My Channel",
        "owner_members" : [change_to_member(test_user1)],
        "all_members" : [change_to_member(test_user1), change_to_member(test_user2), change_to_member(test_user3)]
    }
    assert channel_details(test_user1["token"], test_channel["channel_id"]) == expected

def test_invalid_channel_id():
    '''Tests invalid channel id'''
    database.reset()
    test_user1 = create_login_user(user1)
    with pytest.raises(InputError):
        channel_details(test_user1["token"], 5555555)

def test_not_a_member():
    '''Tests when user is not a member of channel'''
    database.reset()
    test_user1 = create_login_user(user1)
    test_user2 = create_login_user(user2)
    test_channel = channels_create(test_user1["token"], "My Channel", True)
    with pytest.raises(AccessError):
        channel_details(test_user2["token"], test_channel["channel_id"])

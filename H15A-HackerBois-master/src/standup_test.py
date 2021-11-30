'''This module tests standup'''
from datetime import datetime, timedelta, timezone
import time
import pytest
from database import database
from projectDefines import user1, user2
from pytestHelperFunctions import create_login_user
from standup import standup_start, standup_active, standup_send
from channels import channels_create
from channel import channel_invite
from error import InputError, AccessError

def test_standup_start_correct_return():
    '''Tests correct return'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    #Calculating time finished
    length = 1
    time_finish = datetime.utcnow() + timedelta(seconds=length)
    time_finish = time_finish.replace(tzinfo=timezone.utc).timestamp()
    output = standup_start(user1["token"], channel_info["channel_id"], length)
    #Make sure it is within a reasonable delay
    assert abs(output["time_finish"] - time_finish) < 0.001

def test_standup_start_invalid_channel_id():
    '''Tests invalid channel id'''
    database.reset()
    create_login_user(user1)
    channels_create(user1["token"], "MyChannel", True)
    length = 1
    with pytest.raises(InputError):
        standup_start(user1["token"], 6547564, length)

def test_standup_start_already_active():
    '''Tests already active'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    length = 1
    standup_start(user1["token"], channel_info["channel_id"], length)
    with pytest.raises(InputError):
        standup_start(user1["token"], channel_info["channel_id"], length)

def test_standup_active_correct():
    '''Tests active correct'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    length = 1
    standup_start(user1["token"], channel_info["channel_id"], length)
    assert standup_active(user1["token"], channel_info["channel_id"])["is_active"]
    time.sleep(length + 1)
    assert not standup_active(user1["token"], channel_info["channel_id"])["is_active"]

def test_standup_active_invalid_channel():
    '''Tests invalid channel'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    length = 1
    standup_start(user1["token"], channel_info["channel_id"], length)
    with pytest.raises(InputError):
        standup_active(user1["token"], 6547564)

def test_standup_send_invalid_channel():
    '''Tests invalid channel'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    length = 1
    standup_start(user1["token"], channel_info["channel_id"], length)
    with pytest.raises(InputError):
        standup_send(user1["token"], 6547564, "hi")

def test_standup_send_message_too_long():
    '''Tests message too long'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    length = 1
    standup_start(user1["token"], channel_info["channel_id"], length)
    message = "h" * 1001
    with pytest.raises(InputError):
        standup_send(user1["token"], channel_info["channel_id"], message)

def test_standup_send_not_active():
    '''Tests not active'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    with pytest.raises(InputError):
        standup_send(user1["token"], channel_info["channel_id"], "hi")

def test_standup_send_user_not_in_channel():
    '''Tests user not in channel'''
    database.reset()
    create_login_user(user1)
    create_login_user(user2)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    length = 1
    standup_start(user1["token"], channel_info["channel_id"], length)
    message = "hello"
    with pytest.raises(AccessError):
        standup_send(user2["token"], channel_info["channel_id"], message)

def test_standup_send_valid_1_user():
    '''Tests valid user'''
    database.reset()
    create_login_user(user1)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    length = 1
    standup_start(user1["token"], channel_info["channel_id"], length)
    message = "hello"
    assert standup_send(user1["token"], channel_info["channel_id"], message) == {}

def test_standup_send_valid_2_user():
    '''Tests valid user'''
    database.reset()
    create_login_user(user1)
    create_login_user(user2)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    channel_invite(user1["token"], channel_info["channel_id"], user2["u_id"])
    length = 3
    standup_start(user1["token"], channel_info["channel_id"], length)
    message = "hello"
    assert standup_send(user1["token"], channel_info["channel_id"], message) == {}
    assert standup_send(user2["token"], channel_info["channel_id"], message) == {}
    assert standup_send(user1["token"], channel_info["channel_id"], message) == {}
    assert standup_send(user2["token"], channel_info["channel_id"], message) == {}

def test_valid_standup_message():
    '''Tests if the standup message is valid'''
    database.reset()
    create_login_user(user1)
    create_login_user(user2)
    channel_info = channels_create(user1["token"], "MyChannel", True)
    channel_invite(user1["token"], channel_info["channel_id"], user2["u_id"])
    length = 2
    standup_start(user1["token"], channel_info["channel_id"], length)
    message = "hello"
    standup_send(user1["token"], channel_info["channel_id"], message) == {}
    standup_send(user2["token"], channel_info["channel_id"], message) == {}

    channel = database.get_channel_by_id(channel_info['channel_id'])
    user = database.get_user_object(user1["token"])

    assert channel.standup_info['active']
    assert channel.standup_info['start_user'] == user

    time.sleep(3)

    assert not channel.standup_info['active']
    assert channel.standup_info['time_finish'] is None
    assert channel.standup_info['start_user'] is None

    assert len(channel.messages) == 1
    assert channel.messages[0].get_message(user1["u_id"])['message'] == 'Hayden: hello\n\nSam: hello\n'


test_valid_standup_message()

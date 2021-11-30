'''This module tests message sendlater'''
from datetime import datetime, timezone
import time
import math
import pytest
from auth import auth_register, auth_login
from channel import channel_messages
from channels import channels_create
from message import message_send, message_sendlater

from error import AccessError, InputError
from projectDefines import user1, user2
from database import database

def new_user(email, password, name_first, name_last):
    '''Creates new user'''
    auth_register(email, password, name_first, name_last)
    user_data = auth_login(email, password)

    return user_data

def test_valid():
    '''Tests valid'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message for 5 seconds later but should take message_id as soon as called
    time_sent = math.floor(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + 5)
    message = message_sendlater(user_a['token'], channel_id, "Hello World", time_sent)
    message_send(user_a['token'], channel_id, "Test")
    assert message['message_id'] == 0

    #Check that channel only shows the second message send
    channel = channel_messages(user_a['token'], channel_id, 0)['messages']
    assert len(channel) == 1
    assert channel[0]['message_id'] == 1

    #Check 4 seconds later that the channel still only has 1 message
    time.sleep(4)
    channel = channel_messages(user_a['token'], channel_id, 0)['messages']
    assert len(channel) == 1
    assert channel[0]['message_id'] == 1

    #Check 5 seconds later that the message is sent out with the correct message_id
    time.sleep(1)
    channel = channel_messages(user_a['token'], channel_id, 0)['messages']
    assert len(channel) == 2
    assert channel[0]['message_id'] == 0
    assert channel[0]['message'] == "Hello World"
    assert channel[0]['time_created'] == time_sent


def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message for 5 seconds later but should take message_id as soon as called
    time_sent = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + 5
    with pytest.raises(AccessError):
        message_sendlater('invalid token', channel_id, "Hello World", time_sent)

def test_invalid_channel_id():
    '''Tests invalid channel id'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id'] # pylint: disable=unused-variable

    #Send message for 5 seconds later but should take message_id as soon as called
    time_sent = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + 5
    with pytest.raises(InputError):
        message_sendlater(user_a['token'], -1, "Hello World", time_sent)

def test_not_in_channel():
    '''Tests  not in channel'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message for 5 seconds later but should take message_id as soon as called
    time_sent = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + 5
    with pytest.raises(AccessError):
        message_sendlater(user_b['token'], channel_id, "Hello World", time_sent)

def test_message_too_long():
    '''Tests message too long'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message for 5 seconds later but should take message_id as soon as called
    time_sent = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() + 5
    message = 'a' * 1001
    with pytest.raises(InputError):
        message_sendlater(user_a['token'], channel_id, message, time_sent)

def test_past_time_sent():
    '''Tests past time sent'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message for 5 seconds later but should take message_id as soon as called
    time_sent = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp() - 5
    with pytest.raises(InputError):
        message_sendlater(user_a['token'], channel_id, "Hello World", time_sent)

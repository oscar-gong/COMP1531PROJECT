'''This module tests message pin'''
import pytest
from auth import auth_register, auth_login
from channel import channel_join
from channels import channels_create
from message import message_send, message_pin
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

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)

    assert not message.is_pinned
    message_pin(user_a['token'], message_id)

    message = database.get_message_object_by_id(message_id)
    assert message.is_pinned


def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)

    assert not message.is_pinned
    with pytest.raises(AccessError):
        message_pin("invalid_token", message_id)

def test_invalid_message_id():
    '''Tests invalid message id'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)

    assert not message.is_pinned

    with pytest.raises(InputError):
        message_pin(user_a['token'], -1)


def test_not_in_channel():
    '''Tests not in channel'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)

    assert not message.is_pinned
    with pytest.raises(AccessError):
        message_pin(user_b['token'], message_id)


def test_not_owner():
    '''Tests not owner'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']
    channel_join(user_b['token'], channel_id)

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)

    assert not message.is_pinned

    with pytest.raises(InputError):
        message_pin(user_b['token'], message_id)

def test_already_pinned():
    '''Tests already pinned'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)

    assert not message.is_pinned
    message_pin(user_a['token'], message_id)

    with pytest.raises(InputError):
        message_pin(user_a['token'], message_id)

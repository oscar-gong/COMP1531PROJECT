'''This module tests message unreact'''
import pytest
from auth import auth_register, auth_login
from channel import channel_join
from channels import channels_create
from message import message_send, message_react, message_unreact

from error import InputError
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
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']
    channel_join(user_b['token'], channel_id)

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)
    assert message.reacts == []
    message_react(user_b['token'], message_id, 1)
    message_react(user_a['token'], message_id, 1)
    assert len(message.reacts) == 1

    reacts = message.reacts[0]

    assert reacts.get_reacts(user_a["u_id"]) == {
        'react_id': 1,
        'u_ids': [1, 0],
        'is_this_user_reacted': True
        }

    message_unreact(user_a['token'], message_id, 1)
    reacts = message.reacts[0]

    assert reacts.get_reacts(user_a["u_id"]) == {
        'react_id': 1,
        'u_ids': [1],
        'is_this_user_reacted': False
        }

    message_unreact(user_b['token'], message_id, 1)
    reacts = message.reacts[0]

    assert reacts.get_reacts(user_b['u_id']) == {
        'react_id': 1,
        'u_ids': [],
        'is_this_user_reacted': False
        }

def test_unreact_on_no_react():
    '''Tests unreact on no react'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)
    assert message.reacts == []
    with pytest.raises(InputError):
        message_unreact(user_a['token'], message_id, 1)

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
    assert message.reacts == []
    message_react(user_a['token'], 0, 1)

    with pytest.raises(InputError):
        message_unreact(user_a['token'], -1, 1)


def test_invalid_message_id_two():
    '''Tests invalid message id'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    #Create new channel
    channel_id = channels_create(user_b['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_b['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)
    assert message.reacts == []
    message_react(user_b['token'], 0, 1)

    with pytest.raises(InputError):
        message_unreact(user_a['token'], message_id, 1)


def test_invalid_react_id():
    '''Tests invalid react id'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)
    assert message.reacts == []
    message_react(user_a['token'], 0, 1)

    with pytest.raises(InputError):
        message_unreact(user_a['token'], message_id, -1)


def test_double_unreacts():
    '''Tests double unreacts'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])

    #Create new channel
    channel_id = channels_create(user_a['token'], 'Channel 0', True)['channel_id']

    #Send message
    message_id = message_send(user_a['token'], channel_id, "Hello World")['message_id']
    message = database.get_message_object_by_id(message_id)
    assert message.reacts == []
    message_react(user_a['token'], 0, 1)
    message_unreact(user_a['token'], 0, 1)

    reacts = message.reacts

    with pytest.raises(InputError):
        message_unreact(user_a['token'], 0, 1)


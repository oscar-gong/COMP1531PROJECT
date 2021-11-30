'''This module tests admin user remove'''
import pytest
from auth import auth_register, auth_login
from admin import admin_userpermission_change, admin_user_remove
from channel import channel_join, channel_messages
from channels import channels_create
from message import message_send, message_react
from error import AccessError, InputError
from projectDefines import user1, user2
from database import database


def new_user(email, password, name_first, name_last):
    '''Creates new user'''
    auth_register(email, password, name_first, name_last)
    user_data = auth_login(email, password)

    return user_data

def test_valid():
    '''Tests valid user'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    owner = database.get_user_object(user_a['token'])
    member = database.get_user_object(user_b['token'])

    assert owner.permission_id == 1
    assert member.permission_id == 2

    #Get owner and member to join the same channel
    channel_id = channels_create(user_a['token'], 'Test Channel', True)['channel_id']
    channel_join(user_b['token'], channel_id)
    channel = database.get_channel_by_id(channel_id)

    assert channel.member_in_channel(user_b['u_id'])

    #Get owner and member to send message
    #Get member to react to owner message
    msg_id = message_send(user_a['token'], channel_id, "Hello I am user A")['message_id']
    message_send(user_b['token'], channel_id, "Hello user A")
    message_react(user_b['token'], msg_id, 1)
    messages = channel_messages(user_b['token'], channel_id, 0)['messages']

    assert len(messages) == 2
    msg = messages[1]

    assert msg['reacts'][0]['u_ids'][0] == 1

    #Owner remove member
    admin_user_remove(user_a['token'], user_b['u_id'])

    #Checks that member message and reacts are removed
    #Checks that he is removed from the channel and from slackr
    messages = channel_messages(user_a['token'], channel_id, 0)['messages']

    assert len(messages) == 1
    msg = messages[0]

    assert not msg['reacts'][0]['u_ids']
    for message in messages:
        assert message['u_id'] != 1

    assert not channel.member_in_channel(user_b['u_id'])
    assert database.get_user_object(user_b['token']) == "NOT_FOUND"
    assert database.get_user_object_by_id(user_b['u_id']) == "NOT_FOUND"

def test_invalid_token():
    '''Tests when admin token is wrong'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    with pytest.raises(AccessError):
        admin_user_remove("Invalid token", user_b['u_id'])

def test_invalid_admin_2():
    '''Tests when user is not an admin'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    owner = database.get_user_object(user_a['token'])
    member = database.get_user_object(user_b['token'])

    assert owner.permission_id == 1
    assert member.permission_id == 2

    with pytest.raises(AccessError):
        admin_user_remove(user_b['token'], user_a['u_id'])

def test_invalid_user():
    '''Tests when u_id does not exist'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    with pytest.raises(InputError):
        admin_user_remove(user_a['token'], -1)

def test_only_owner():
    '''Tests when the only owner tries to remove himself'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    with pytest.raises(InputError):
        admin_user_remove(user_a['token'], user_a['u_id'])

    admin_userpermission_change(user_a['token'], user_b['u_id'], 1)
    admin_user_remove(user_a['token'], user_a['u_id'])

    assert database.get_user_object(user_a['token']) == "NOT_FOUND"
    assert database.get_user_object_by_id(user_a['u_id']) == "NOT_FOUND"

    with pytest.raises(InputError):
        admin_user_remove(user_b['token'], user_b['u_id'])


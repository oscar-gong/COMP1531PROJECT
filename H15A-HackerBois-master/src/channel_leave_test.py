'''This module tests channel leave'''
import pytest
from channel import channel_join, channel_leave
from channels import channels_create
from error import InputError, AccessError
from auth import auth_register, auth_login
from projectDefines import user1, user2
from database import database

def test_valid_channel():
    '''Tests valid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)
    channel_join(user['token'], channel_id['channel_id'])
    assert channel_leave(channel_owner['token'], channel_id['channel_id']) == {}
    #Assume that the function has successfully run with a valid channel hence returning something.
    assert channel_leave(user['token'], channel_id['channel_id']) == {}

def test_invalid_channel():
    '''Tests invalid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    #Since an invalid channel id is inputted in the argument, it should raise an InputError
    with pytest.raises(InputError):
        channel_leave(user['token'], None)

def test_user_exists_in_channel():
    '''Tests user exists in channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)
    channel_join(user['token'], channel_id['channel_id'])
    #function has successfully run with a valid user in channel hence returning something.
    assert channel_leave(user['token'], channel_id['channel_id']) is not None

def test_user_not_in_channel():
    '''Tests user not in channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)
     #Since the user did not join the channel, it should raise an AccessError
    with pytest.raises(AccessError):
        channel_leave(user['token'], channel_id['channel_id'])

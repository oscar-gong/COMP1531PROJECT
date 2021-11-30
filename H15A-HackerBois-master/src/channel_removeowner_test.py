'''This module tests channel removeowner'''
import pytest
from channel import channel_join, channel_addowner, channel_removeowner
from channels import channels_create
from error import InputError, AccessError
from auth import auth_register, auth_login
from projectDefines import user1, user2
from database import database

def test_real_owner():
    '''Tests real owner'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)['channel_id']
    channel_join(user['token'], channel_id)
    channel_addowner(channel_owner['token'], channel_id, user['u_id'])
    #Assume that the function has successfully run with a real owner hence returning something.
    assert channel_removeowner(channel_owner['token'], channel_id, user['u_id']) is not None

def test_fake_owner():
    '''Tests fake owner'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)
    channel_join(user['token'], channel_id['channel_id'])
    #regular user attempting to run the removeowner function should raise AccessError
    with pytest.raises(AccessError):
        channel_removeowner(user['token'], channel_id['channel_id'], channel_owner['u_id'])

def test_valid_channel():
    '''Tests valid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)['channel_id']
    channel_join(user['token'], channel_id)
    channel_addowner(channel_owner['token'], channel_id, user['u_id'])
    #Assume that the function has successfully run with a valid channel hence returning something.
    assert channel_removeowner(channel_owner['token'], channel_id, user['u_id']) is not None

def test_invalid_channel():
    '''Tests invalid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    #Since an invalid channel id is inputted in the argument, it should raise an InputError
    with pytest.raises(InputError):
        channel_removeowner(user['token'], None, user['u_id'])

def test_already_not_owner_of_channel():
    '''Tests already not owner of channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)
    channel_join(user['token'], channel_id['channel_id'])
    #Attempting to removeowner on a user who is not currently an owner should raise InputError.
    with pytest.raises(InputError):
        channel_removeowner(channel_owner['token'], channel_id['channel_id'], user['u_id'])

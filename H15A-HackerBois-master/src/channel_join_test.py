'''This module tests channel join'''
import pytest
from channel import channel_join
from channels import channels_create
from error import InputError, AccessError
from auth import auth_register, auth_login
from projectDefines import user1, user2, user3
from database import database

def test_valid_channel():
    '''Tests valid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)
    #Assume that the function has successfully run with a valid channel hence returning something.
    assert channel_join(user['token'], channel_id['channel_id']) is not None

def test_invalid_channel():
    '''Tests invalid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    #Since an invalid channel id is inputted in the argument, it should raise an InputError
    with pytest.raises(InputError):
        channel_join(user['token'], None)

    #Invalid channel_id
    with pytest.raises(InputError):
        channel_join(user['token'], -0.1)


def test_public_channel():
    '''Tests public channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', True)
    #The user should be able to join a public channel hence returning something.
    assert channel_join(user['token'], channel_id['channel_id']) is not None

def test_private_channel():
    '''Tests private channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    auth_register(user3['email'], user3['password'], user3['name_first'], user3['name_last'])

    channel_owner = auth_login(user1['email'], user1['password'])
    user = auth_login(user2['email'], user2['password'])
    user_3 = auth_login(user3['email'], user3['password'])
    channel_id = channels_create(channel_owner['token'], 'newChannel', False)
    #Since the channel is private, a regular user should not be able to join
    #hence raising an AccessError.
    with pytest.raises(AccessError):
        channel_join(user['token'], channel_id['channel_id'])
    with pytest.raises(AccessError):
        channel_join(user_3['token'], channel_id['channel_id'])

'''This module tests channels create'''
import pytest
import auth
#import channel
import channels
from error import AccessError, InputError
from projectDefines import user1 #user1 is just dummy user for testing
from database import database

def test_invalid_input():
    '''Tests invalid input'''
    database.reset()
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_data = auth.auth_login(user1['email'], user1['password'])
    #Name is more than 20 characters
    with pytest.raises(InputError):
        channels.channels_create(user_data['token'], 'A'*21, True)

def test_valid_input():
    '''Tests valid input'''
    database.reset()
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_data = auth.auth_login(user1['email'], user1['password'])
    chs_name = 'ValidName'
    chs1_1_name = 'PrivateName'

    chs = channels.channels_create(user_data['token'], chs_name, True)
    assert chs == {
        "channel_id": chs['channel_id']
    }

    chs_1 = channels.channels_create(user_data['token'], chs1_1_name, False)
    assert chs_1 == {
        "channel_id": chs_1['channel_id']
    }

    #Since a user has created 2 channels
    #Upon User list all , User should see them
    ch_detail = channels.channels_listall(user_data['token'])

    assert ch_detail == {
        "channels": [{"channel_id":chs['channel_id'], "name":chs_name},
                     {"channel_id":chs_1['channel_id'], "name":chs1_1_name}]
    }

    for it_detail in ch_detail['channels']:
        if(it_detail['channel_id'] in [chs['channel_id'], chs_1['channel_id']]):
            assert it_detail['name'] in [chs_name, chs1_1_name]

def test_same_name():
    '''Tests same name'''
    database.reset()
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_data = auth.auth_login(user1['email'], user1['password'])

     #A channel can not be created twice with the same name
    #Assume InputError
    channels.channels_create(user_data['token'], 'ValidName', True)

    with pytest.raises(InputError):
        channels.channels_create(user_data['token'], 'ValidName', True)

def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth.auth_login(user1['email'], user1['password'])

    #Invalid_token is passed in
    with pytest.raises(AccessError):
        channels.channels_create('Invalid_token', 'ValidName', True)

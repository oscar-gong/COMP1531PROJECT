'''This module tests channels listall'''
import pytest
import auth
import channels
from error import AccessError
from projectDefines import user1 #user1 is just dummy user for testing
from database import database
def test_empty_channels():
    '''Tests empty channels'''
    database.reset()
    #Get new user
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_data = auth.auth_login(user1['email'], user1['password'])
    #User does not create channel

    # List of channels
    chs = channels.channels_listall(user_data['token'])


    #Should have empty string since the user is not creating channel
    assert chs['channels'] == []

def test_one_channel():
    '''Tests one channel'''
    database.reset()
    #Get new user
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_data = auth.auth_login(user1['email'], user1['password'])

    #User does create a channel which is public
    ch_create = channels.channels_create(user_data['token'], 'Anyname', True)
    assert ch_create != {}

    # List of channels
    chs = channels.channels_listall(user_data['token'])
    #assume the first channel is created by user
    assert chs != {}
    assert chs['channels'] != []
    length_of_channel = len(chs['channels'])
    assert length_of_channel == 1
    #loop through the list of dictionaries
    for channel in chs['channels']:
        if channel['channel_id'] == ch_create['channel_id']:
            assert channel['name'] == 'Anyname'


def test_ten_channels():
    '''Tests ten channels'''
    database.reset()
    #Get new user
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_data = auth.auth_login(user1['email'], user1['password'])
    #User creates 10 channels
    for i in range(10):
        channel_name = 'Anyname' + str(i)
        ch_create = channels.channels_create(user_data['token'], channel_name, True)
        assert ch_create != {}
        chs = channels.channels_listall(user_data['token'])
        assert chs != {}

        length_of_channel = len(chs['channels'])
        #Number of channels start from 1
        assert length_of_channel == i + 1

        #Assuming the system has no channels and we create
        channel = chs['channels'][i]
        assert channel['channel_id'] == ch_create['channel_id']
        assert channel['name'] == channel_name
    #User does create a channel



def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    #Get new user
    auth.auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_data = auth.auth_login(user1['email'], user1['password'])

    #User does create a channel which is public
    ch_create = channels.channels_create(user_data['token'], 'Anyname', True)
    assert ch_create != {}

    #List of channels
    #Assuming when input is a invalid_token then InputError is raised
    with pytest.raises(AccessError):
        channels.channels_listall('Invalid_token')

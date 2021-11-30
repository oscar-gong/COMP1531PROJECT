'''This module tests channels list'''
from channels import channels_create, channels_list
from auth import auth_register, auth_login
from projectDefines import user1
from database import database

def test_valid_user():
    '''Tests valid user'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channel_id = channels_create(user['token'], 'newChannel', True)
    channels = channels_list(user['token'])['channels']
    channel = channels[0]
    assert channel['channel_id'] == channel_id['channel_id']
    assert channel['name'] == 'newChannel'
    #Assuming that the function successfully ran with a valid user.
    assert channels_list(user['token']) is not None or channels_list(user['token']) != {}

def test_invalid_user():
    '''Tests invalid user'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channels_create(user['token'], 'newChannel', True)
     #Assuming that the function does not run or returns None when the user does not exist.
    assert channels_list(None) is None

def test_no_channels():
    '''Tests no channels'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    assert (channels_list(user['token'])['channels']) == []

def test_one_channel():
    '''Tests one channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channel_id = channels_create(user['token'], 'Channel 1', True)
    assert channel_id != {} #should not be empty
    channels = channels_list(user['token'])['channels']
    assert len(channels) == 1 #amount of channels should be 1
    channel = channels[0]
    assert channel['channel_id'] == channel_id['channel_id']
    assert channel['name'] == 'Channel 1'

def test_ten_channels():
    '''Tests ten channels'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    for i in range(10): #loop 10 times creating new channels
        channel_id = channels_create(user['token'], 'Channel '+ str(1+i), True)
        assert channel_id != {}
        channels = channels_list(user['token'])['channels']
        assert len(channels) == i + 1
        channel = channels[i]
        #check if the created channel id matches
        assert channel['channel_id'] == channel_id['channel_id']
        #check if the created channel name matches
        assert channel['name'] == 'Channel '+ str(1+i)

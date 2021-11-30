'''This module tests channel messages'''
import pytest
from channel import channel_join, channel_messages
from channels import channels_create
from error import InputError, AccessError
from auth import auth_register, auth_login
from message import message_send
from projectDefines import user1, user2
from database import database

def test_valid_channel():
    '''Tests valid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channel_id = channels_create(user['token'], 'newChannel', True)
    channel_join(user['token'], channel_id["channel_id"])
    message_send(user['token'], channel_id["channel_id"], 'hello')
    #Assume that the function has successfully run with a valid channel hence returning something.
    assert channel_messages(user['token'], channel_id["channel_id"], 0) is not None

    for i in range(60):
        message_send(user['token'], channel_id["channel_id"], 'hello' + str(i))

    assert channel_messages(user['token'], channel_id["channel_id"], 0) is not None

def test_invalid_channel():
    '''Tests invalid channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    #Since an invalid channel id is inputted in the argument, it should raise an InputError
    with pytest.raises(InputError):
        channel_messages(user['token'], None, 0)

def test_valid_start():
    '''Tests valid start'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channel_id = channels_create(user['token'], 'newChannel', True)
    channel_join(user['token'], channel_id["channel_id"])
    message_send(user['token'], channel_id["channel_id"], 'hello')
    #start should start at 0 and will not go below.
    assert channel_messages(user['token'], channel_id["channel_id"], 0)['start'] >= 0

def test_invalid_start():
    '''Tests invalid start'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channel_id = channels_create(user['token'], 'newChannel', True)
    channel_join(user['token'], channel_id["channel_id"])
    #Total messages in the channel is now 1
    message_send(user['token'], channel_id["channel_id"], 'hello')
    #raise input error when start is greater than the amount of messages in the channel.
    with pytest.raises(InputError):
        # 100>1 hence raise InputError.
        channel_messages(user['token'], channel_id["channel_id"], 100)

def test_user_exists_in_channel():
    '''Tests user exists in channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channel_id = channels_create(user['token'], 'newChannel', True)
    channel_join(user['token'], channel_id["channel_id"])
    message_send(user['token'], channel_id["channel_id"], 'hello')
    #the function has successfully run with a user in the channel hence returning something.
    assert channel_messages(user['token'], channel_id["channel_id"], 0) is not None

def test_user_not_in_channel():
    '''Tests user not in channel'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_in_channel = auth_login(user1['email'], user1['password'])
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    user = auth_login(user2['email'], user2['password'])
    channel_id = channels_create(user_in_channel['token'], 'newChannel', True)
    message_send(user_in_channel['token'], channel_id["channel_id"], 'hello')
    with pytest.raises(AccessError):
        #since the user did not join the channel, it should raise an AccessError
        channel_messages(user['token'], channel_id["channel_id"], 0)

def test_correct_output_size():
    '''Tests correct output size'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    channel_id = channels_create(user['token'], 'newChannel', True)
    channel_join(user['token'], channel_id["channel_id"])
    message_send(user['token'], channel_id["channel_id"], 'hello')
     #checks on the output length of the function
    assert len(channel_messages(user['token'], channel_id["channel_id"], 0)) == 3
     #checks on the length of an individual message.
    assert len(channel_messages(user['token'], channel_id["channel_id"], 0)['messages'][0]) == 6

'''This module tests message send'''
import pytest
import auth
import channel
import channels
import message
from error import AccessError, InputError
from projectDefines import user1 as test #user1 is just dummy user for testing
from projectDefines import user2 as test1 #user1 is just dummy user for testing
from database import database

def test_valid():
    '''Tests valid'''
    database.reset()
    #Get new user
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user_data = auth.auth_login(test['email'], test['password'])

    chs = channels.channels_create(user_data['token'], 'Whatever', True)
    mes = message.message_send(user_data['token'], chs['channel_id'], 'Hey every one!')

    #The most recent message_id should be the same
    start = 0
    ch_m = channel.channel_messages(user_data['token'], chs['channel_id'], start)
    assert ch_m['messages'] != []
    assert mes['message_id'] == ch_m['messages'][start]['message_id']


def test_invalid_input():
    '''Tests invalid input'''
    database.reset()
    #Get new user
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user_data = auth.auth_login(test['email'], test['password'])

    chs = channels.channels_create(user_data['token'], 'Whatever', True)

    #Assum message is more than 1000 characters
    with pytest.raises(InputError):
        message.message_send(user_data['token'], chs['channel_id'], 'A'*1001)

    #Assume Invalid token will have input error
    with pytest.raises(AccessError):
        message.message_send('Invalid_token', chs['channel_id'], 'Hey every one!')

    #Assume Invalid channl_id will have input error
    with pytest.raises(AccessError):
        message.message_send(user_data['token'], -100, 'Hey every one!')


def test_invalid_access():
    '''Tests invalid access'''
    database.reset()
    #Get new user
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user_data = auth.auth_login(test['email'], test['password'])

    #New user2 who has not joined the channel is trying to send message
    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user_data_1 = auth.auth_login(test1['email'], test1['password'])

    #First user creates the channel
    chs = channels.channels_create(user_data['token'], 'Whatever', True)

    #Second user is not in the channel but trying to send
    #user_data = user 1(in the channel)
    #User_data_1 = user 2(not in the channel)

    with pytest.raises(AccessError):
        message.message_send(user_data_1['token'], chs['channel_id'], 'hell ya')

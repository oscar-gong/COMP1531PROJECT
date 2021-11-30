'''This module tests message remove'''
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

    #User creats channel
    chs = channels.channels_create(user_data['token'], 'Whatever', True)

    #User sends messages
    message.message_send(user_data['token'], chs['channel_id'], 'Hey every one!')

    mes = message.message_send(user_data['token'], chs['channel_id'], 'TODAY is a good day')

    #User remove it himself
    back = message.message_remove(user_data['token'], mes['message_id'])
    assert back == {}

    start = 0
    msg = channel.channel_messages(user_data['token'], chs['channel_id'], start)

    #Can never find this message
    for it_mes in msg['messages']:
        assert it_mes['message'] != 'TODAY is a good day'



def test_invalid_input():
    '''Tests invalid input'''
    database.reset()
    #Get new user
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user_data = auth.auth_login(test['email'], test['password'])

    #Create channel
    chs = channels.channels_create(user_data['token'], 'Whatever', True)
    #Send
    mes = message.message_send(user_data['token'], chs['channel_id'], 'Hey every one!')
    #Remove
    back = message.message_remove(user_data['token'], mes['message_id'])
    assert back == {}

    #user is not sending message
    #Can not remove a message which is no longer existing
    with pytest.raises(InputError):
        message.message_remove(user_data['token'], mes['message_id'])


def test_invalid_access():
    '''Tests invalid access'''
    database.reset()
    #Get new user
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user_data = auth.auth_login(test['email'], test['password'])

    #Create channel
    chs = channels.channels_create(user_data['token'], 'Whatever', True)
    #user says something in channel which is the owner
    msg = message.message_send(user_data['token'], chs['channel_id'], 'Hey every one!')
    assert msg != {}

    #login second user
    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user_data_1_login = auth.auth_login(test1['email'], test1['password'])
    #User_data_1 is not the owner of the channel
    #Remove

    #Assum message id_1 exists as user sent before
    #But user1 is not in the channel which is not the owner of the channel

    with pytest.raises(AccessError):
        message.message_remove(user_data_1_login['token'], msg['message_id'])


    #User2 wants join the channel
    channel.channel_join(user_data_1_login['token'], chs['channel_id'])


    #user says something agaign
    msg_1 = message.message_send(user_data['token'], chs['channel_id'], 'WHO is this guy?')

    #User1 is trying to remove the messeage sent by user

    #Get AccessError
    with pytest.raises(AccessError):
        message.message_remove(user_data_1_login['token'], msg_1['message_id'])


def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    #Get new user
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user_data = auth.auth_login(test['email'], test['password'])

    #Create Channel
    chs = channels.channels_create(user_data['token'], 'Whatever', True)
    #Send
    mes = message.message_send(user_data['token'], chs['channel_id'], 'Hey every one!')

    #Dont need to remove twice

    #Invalid token
    with pytest.raises(AccessError):
        message.message_remove('Invalid_token', mes['message_id'])

def test_invalid_message_id():
    '''Tests invalid message id'''
    database.reset()
    #Get new user
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user_data = auth.auth_login(test['email'], test['password'])

    #Create channel
    chs = channels.channels_create(user_data['token'], 'Whatever', True)
    #Send
    mes = message.message_send(user_data['token'], chs['channel_id'], 'Hey every one!')

    #Remove
    back = message.message_remove(user_data['token'], mes['message_id'])
    assert back == {}

    #Invalid message_id
    with pytest.raises(InputError):
        message.message_remove(user_data['token'], -200)

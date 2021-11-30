'''This module tests message edit'''
import pytest
import auth
import channel
import channels
import message
from error import AccessError, InputError
from projectDefines import user1 as test #user1 is just dummy user for testing
from projectDefines import user2 as test1 #user1 is just dummy user for testing
from projectDefines import user3 as test2
from database import database

def test_valid():
    '''Tests valid'''
    database.reset()
    #Creating 3 users
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user = auth.auth_login(test['email'], test['password'])

    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user1 = auth.auth_login(test1['email'], test1['password'])

    auth.auth_register(test2['email'], test2['password'], test2['name_first'], test2['name_last'])
    user2 = auth.auth_login(test2['email'], test2['password'])
    #User creats channel
    chs = channels.channels_create(user['token'], 'Whatever', True)

    invite = channel.channel_invite(user['token'], chs['channel_id'], user1['u_id'])
    assert invite == {}
    invite = channel.channel_invite(user['token'], chs['channel_id'], user2['u_id'])
    assert invite == {}

    channel.channel_addowner(user['token'], chs['channel_id'], user1['u_id'])
    channel.channel_addowner(user['token'], chs['channel_id'], user2['u_id'])

    #User sends message
    mes = message.message_send(user['token'], chs['channel_id'], 'Hey every one!')

    #User edit it
    back = message.message_edit(user['token'], mes['message_id'], 'This is the edited message')
    assert back == {}


    #User1 sends message
    mes1 = message.message_send(user1['token'], chs['channel_id'], 'How are ya doing?')

    #User1 edit it
    back1 = message.message_edit(user1['token'], mes1['message_id'], 'Nah dont worry')
    assert back1 == {}

    #User2 sends message
    mes2 = message.message_send(user2['token'], chs['channel_id'], 'This is a sentence which will be edited')

    #User2 edit it
    back2 = message.message_edit(user2['token'], mes2['message_id'], 'blabla')
    assert back2 == {}

    start = 0
    msg = channel.channel_messages(user['token'], chs['channel_id'], start)

    sentence = ['This is the edited message', 'Nah dont worry', 'blabla']
    for it_mes in msg['messages']:
        if it_mes['message_id'] in [mes['message_id'], mes1['message_id'], mes2['message_id']]:
            assert it_mes['message'] in sentence

    #User2 edit it again

    #raise error when edit with blank string
    with pytest.raises(InputError):
        back2 = message.message_edit(user2['token'], mes2['message_id'], '')

    #updating status
    msg = channel.channel_messages(user['token'], chs['channel_id'], start)

    #found message_id of 'blabla' back
    for it_mes in msg['messages']:
        if it_mes['message_id'] in [mes['message_id'], mes1['message_id'], mes2['message_id']]:
            assert it_mes['message'] in sentence


def test_access_error_case0():
    '''Tests access error'''
    database.reset()
    #case0 user is not edting thier own message (within the channel)

    #Creating test users
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user = auth.auth_login(test['email'], test['password'])

    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user1 = auth.auth_login(test1['email'], test1['password'])


    chs = channels.channels_create(user['token'], 'Whatever', True)

    #User1 has been invited(wil be in the channel)
    #User2 has not been invited (will not be in the channel)
    invite = channel.channel_invite(user['token'], chs['channel_id'], user1['u_id'])
    assert invite == {}
    #User sends message
    mes = message.message_send(user['token'], chs['channel_id'], 'Hey every one!')

    #User1 is trying edit message which was sent by User
    #Which gives error
    with pytest.raises(AccessError):
        message.message_edit(user1['token'], mes['message_id'], 'I want to edit but I can not')


def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    #Creating test users
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user = auth.auth_login(test['email'], test['password'])

    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user1 = auth.auth_login(test1['email'], test1['password'])

    auth.auth_register(test2['email'], test2['password'], test2['name_first'], test2['name_last'])
    user2 = auth.auth_login(test2['email'], test2['password'])


    chs = channels.channels_create(user['token'], 'Whatever', True)

    #Invite user1 and user2
    invite = channel.channel_invite(user['token'], chs['channel_id'], user1['u_id'])
    assert invite == {}

    invite = channel.channel_invite(user['token'], chs['channel_id'], user2['u_id'])
    assert invite == {}

    #User sends message
    mes = message.message_send(user['token'], chs['channel_id'], 'Good day!')

    #Invalid token is passed in
    with pytest.raises(AccessError):
        message.message_edit('Invalid_token', mes['message_id'], 'I want to edit but I can not')

def test_invalid_message_id():
    '''Tests invalid message id'''
    database.reset()
    #Creating test users
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user = auth.auth_login(test['email'], test['password'])

    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user1 = auth.auth_login(test1['email'], test1['password'])

    auth.auth_register(test2['email'], test2['password'], test2['name_first'], test2['name_last'])
    user2 = auth.auth_login(test2['email'], test2['password'])

    chs = channels.channels_create(user['token'], 'Whatever', True)

    #Invite user1 and user2
    invite = channel.channel_invite(user['token'], chs['channel_id'], user1['u_id'])
    assert invite == {}

    invite = channel.channel_invite(user['token'], chs['channel_id'], user2['u_id'])
    assert invite == {}

    #User sends message
    message.message_send(user['token'], chs['channel_id'], 'Good day!')

    #Invaide message_id has been entered should raise InputError
    with pytest.raises(InputError):
        message.message_edit(user['token'], -10, 'I want to edit but I can not')



def test_access_error_case1():
    '''Tests access error'''
    database.reset()
    #case1 user is not edting the message (outside of the channel)
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user = auth.auth_login(test['email'], test['password'])

    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user1 = auth.auth_login(test1['email'], test1['password'])

    auth.auth_register(test2['email'], test2['password'], test2['name_first'], test2['name_last'])
    user2 = auth.auth_login(test2['email'], test2['password'])

    chs = channels.channels_create(user['token'], 'Whatever', True)

    #User1 has been invited(wil be in the channel)
    #User2 has not been invited (will not be in the channel)
    invite = channel.channel_invite(user['token'], chs['channel_id'], user1['u_id'])
    assert invite == {}

    #User sends message
    mes = message.message_send(user['token'], chs['channel_id'], 'Hey every one!')

    #case2 user outside of the channel is trying to edit something in the channel
    with pytest.raises(AccessError):
        message.message_edit(user2['token'], mes['message_id'], 'I want to edit but I can not')


def test_access_error_case2():
    '''Tests access error'''
    database.reset()
    #case2 user is just a memember not owner (within the channel)
    auth.auth_register(test['email'], test['password'], test['name_first'], test['name_last'])
    user = auth.auth_login(test['email'], test['password'])

    auth.auth_register(test1['email'], test1['password'], test1['name_first'], test1['name_last'])
    user1 = auth.auth_login(test1['email'], test1['password'])

    chs = channels.channels_create(user['token'], 'Whatever', True)

    #User1 has been invited(wil be in the channel)
    invite = channel.channel_invite(user['token'], chs['channel_id'], user1['u_id'])
    assert invite == {}
    #User sends message
    mes = message.message_send(user['token'], chs['channel_id'], 'Hey every one!')

    #User1 is not admin or owner of this channel as it is invited by User so it is member
    with pytest.raises(AccessError):
        message.message_edit(user1['token'], mes['message_id'], 'gg')

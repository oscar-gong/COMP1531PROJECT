"""This module is designed for the system_test"""
import json
import urllib
import time
from datetime import datetime, timezone
import flask # pylint: disable=unused-import
import pytest
from projectDefines import user1, user2, user3

#Base url
BASE_URL = 'http://127.0.0.1:5052'
#Custom headers for POST method
#JSON type payload
CUSTOM_HEADER = {
    "Content-Type": "application/json"
}
#Testing U_id
USER_UID_1 = ''
USER_UID_2 = ''
USER_UID_3 = ''
#Testing token
USER_TOKEN_1 = ''
USER_TOKEN_2 = ''
USER_TOKEN_3 = ''
def test_workspace_reset():
    '''Reset everthing make sure the work space is clean'''
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

def test_initialisation(): # pylint: disable=too-many-statements
    '''Initialises tests'''
    global USER_UID_1, USER_UID_2, USER_UID_3 # pylint: disable=global-statement
    global USER_TOKEN_1, USER_TOKEN_2, USER_TOKEN_3 # pylint: disable=global-statement
    #Register user1
    value = {
        "email":user1['email'],
        "password":user1['password'],
        "name_first":user1['name_first'],
        "name_last":user1['name_last']
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    USER_UID_1 = json_response['u_id']
    USER_TOKEN_1 = json_response['token']
    assert USER_UID_1 == 0
    assert USER_TOKEN_1 is not None

    #Regiseter user2
    value = {
        "email":user2['email'],
        "password":user2['password'],
        "name_first":user2['name_first'],
        "name_last":user2['name_last']
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)

    USER_UID_2 = json_response['u_id']
    USER_TOKEN_2 = json_response['token']
    assert USER_UID_2 == 1
    assert USER_TOKEN_2 is not None

    #Regiseter user3
    value = {
        "email":user3['email'],
        "password":user3['password'],
        "name_first":user3['name_first'],
        "name_last":user3['name_last']
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)

    USER_UID_3 = json_response['u_id']
    USER_TOKEN_3 = json_response['token']
    assert USER_UID_3 == 2
    assert USER_TOKEN_3 is not None


    #User1 creates a channel
    value = {
        "token":USER_TOKEN_1,
        "name":'channel1',
        "is_public":True
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)

    assert json_response['channel_id'] == 0

    #User1 creates a channel
    value = {
        "token":USER_TOKEN_1,
        "name":'channel1_1',
        "is_public":True
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)

    assert json_response['channel_id'] == 1

    #User2 creates a channel
    value = {
        "token":USER_TOKEN_2,
        "name":'channel2',
        "is_public":True
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['channel_id'] == 2


    #User3 creates a channel
    value = {
        "token":USER_TOKEN_3,
        "name":'channel3',
        "is_public":False
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channels/create", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['channel_id'] == 3

#message.py
def test_message_send():
    '''Tests message send'''
    #User 1 sends msg
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "message":'Hello!'
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/send", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['message_id'] == 0

    #User2 sends msg
    value = {
        "token":USER_TOKEN_2,
        "channel_id":2,
        "message":'Hello!'
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/send", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['message_id'] == 1

    #User3 sends msg
    value = {
        "token":USER_TOKEN_3,
        "channel_id":3,
        "message":'Hello!'
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/send", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['message_id'] == 2

    #Error checking

    #Message is too long
    value = {
        "token":USER_TOKEN_3,
        "channel_id":3,
        "message":'a'*1001
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Not a member
    value = {
        "token":USER_TOKEN_2,
        "channel_id":3,
        "message":'hi'
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/send", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_message_react():
    '''Tests message react'''
    #User1 is reacting to its own message
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
        "react_id":1
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/react", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #User1 is inviting user2 in his channel
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "u_id":USER_UID_2
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channel/invite", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #User2 is reacting to user1's message
    value = {
        "token":USER_TOKEN_2,
        "message_id":0,
        "react_id":1
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/react", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #User2 is inviting user3
    value = {
        "token":USER_TOKEN_2,
        "channel_id":0,
        "u_id":USER_UID_3
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/channel/invite", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}


    #Error checking

    #Message_id is not in the channel which the user is in
    value = {
        "token":USER_TOKEN_1,
        "message_id":10,
        "react_id":1
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/react", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #invalid react id
    value = {
        "token":USER_TOKEN_3,
        "message_id":0,
        "react_id":2
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/react", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Can not react again

    #User1 is reacting to its own message
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
        "react_id":1
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/react", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_message_unreact():
    '''Tests message unreact'''
    #User1 is unreacting to its own message
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
        "react_id":1
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/unreact", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}


    #Error checking

    #Message_id is not in the channel which the user is in
    value = {
        "token":USER_TOKEN_2,
        "message_id":10,
        "react_id":1
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/unreact", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #invalid unreact id
    value = {
        "token":USER_TOKEN_2,
        "message_id":0,
        "react_id":2
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/unreact", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Can not unreact again

    #User1 is reacting to its own message
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
        "react_id":1
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/unreact", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def test_message_pin():
    '''Tests message pin'''
    #User1 pinned message_id 0
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #User2 sends a message
    value = {
        "token":USER_TOKEN_2,
        "channel_id":0,
        'message':"kool_kids"
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/send", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    msg_id = json_response['message_id']

    #User1 pinned the msg sent by user2

    value = {
        "token":USER_TOKEN_1,
        "message_id":msg_id,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #Error checking

    #Invalid message_id
    value = {
        "token":USER_TOKEN_1,
        "message_id":-100,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Not a owner
    value = {
        "token":USER_TOKEN_2,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Msg is already pinned
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #User3 is trying to pin the message
    value = {
        "token":USER_TOKEN_3,
        "message_id":msg_id,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def test_message_unpin():
    '''Tests message unpin'''
    #User1 unpinn message_id 0
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/unpin", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #User1 pinned it again
    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}


    #Error checking

    #Invalid message_id
    value = {
        "token":USER_TOKEN_1,
        "message_id":-100,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/unpin", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #User2 is trying to unpin but he is not the owner
    value = {
        "token":USER_TOKEN_2,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/unpin", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #msg is already unpinned

    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/unpin", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    value = {
        "token":USER_TOKEN_1,
        "message_id":0,
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/unpin", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)


def test_message_remove():
    '''Tests message remove'''
    value = {
        "token":USER_TOKEN_1,
        "message_id":0
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/remove", data, CUSTOM_HEADER, method='DELETE')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    value = {
        "token":USER_TOKEN_1,
        "message_id":2
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/remove", data, CUSTOM_HEADER, method='DELETE')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #Message no longer exist
    value = {
        "token":USER_TOKEN_1,
        "message_id":0
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/remove", data, CUSTOM_HEADER, method='DELETE')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #User3 is trying to remove the message which user3 is not the member of
    value = {
        "token":USER_TOKEN_3,
        "message_id":1
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/remove", data, CUSTOM_HEADER, method='DELETE')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_message_edit():
    '''Tests message edit'''
    #User 1 is sending a message
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "message":'Hello!'
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/send", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['message_id'] == 4

    #User1 is trying to edit
    value = {
        "token":USER_TOKEN_1,
        "message_id":json_response['message_id'],
        "message":'all good'
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/edit", data, CUSTOM_HEADER, method='PUT')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #Error checking

    #User3 is nether the owner of the slackr nor the memer of the channel
    #Which the message is in
    value = {
        "token":USER_TOKEN_3,
        "message_id":3,
        'message':"Can I edit ?"
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/edit", data, CUSTOM_HEADER, method='PUT')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_message_sendlater():
    '''Tests message sendlater'''
    #User 1 is sending a message by 5 seconds after
    #Unit of sec
    two_sec_unix = (datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 2
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "message":'This msg is from the past 2 sec',
        "time_sent":two_sec_unix

    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/message/sendlater", data, CUSTOM_HEADER, method='POST') # pylint: disable=line-too-long
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['message_id'] == 5
    msg_id = json_response['message_id']

    time.sleep(2.5)


    #The msg_id should exist
    value = {
        "token":USER_TOKEN_1,
        "message_id":msg_id,
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/pin", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}


    #Error checking

    #Invalid channel_id
    two_sec_unix = (datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 2
    value = {
        "token":USER_TOKEN_1,
        "channel_id":-100,
        "message":'This msg is from the past 2 sec',
        "time_sent":two_sec_unix
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/sendlater", data, CUSTOM_HEADER, method='POST') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Invalid msg
    two_sec_unix = (datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 2
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "message":'This msg is from the past 2 sec'*2000,
        "time_sent":two_sec_unix
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/sendlater", data, CUSTOM_HEADER, method='POST') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #past time
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "message":'This msg is from the past 2 sec',
        "time_sent":-100000000
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/sendlater", data, CUSTOM_HEADER, method='POST') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #User3 is trying to send

    #User3 left the channel
    value = {
        "token":USER_TOKEN_3,
        "channel_id":0,
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/leave", data, CUSTOM_HEADER, method='POST') # pylint: disable=line-too-long
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #User3 is trying to send msg outside of the channel

    two_sec_unix = (datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()) + 2
    value = {
        "token":USER_TOKEN_3,
        "channel_id":0,
        "message":'This msg is from the past 2 sec',
        "time_sent":two_sec_unix
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/message/sendlater", data, CUSTOM_HEADER, method='POST') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

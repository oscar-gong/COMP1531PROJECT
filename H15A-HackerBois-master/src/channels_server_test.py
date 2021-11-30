"""This module is designed for the system_test"""
import json
import urllib
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
    '''Reset everything make sure the work space is clean'''
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

def test_initialisation():
    '''Test initialisation'''
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

    #Register user2
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

    #Register user3
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

def test_channels_create():
    '''Tests channels create'''

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
    #Invalid name
    value = {
        "token":USER_TOKEN_1,
        "name":'a'*21,
        "is_public":True
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channels/create", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)
def test_channels_list():
    '''Tests channels list'''
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?{query_string}")
    payload = json.load(response)
    for idx, channels in enumerate(payload['channels']):
        assert channels['channel_id'] == idx
        assert channels['name'] in ['channel1', 'channel1_1']

def test_channels_listall():
    '''Tests channels listall'''
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channels/list?{query_string}")
    payload = json.load(response)
    for idx, channels in enumerate(payload['channels']):
        assert channels['channel_id'] == idx
        assert channels['name'] in ['channel1', 'channel1_1', 'channel2', 'channel3']

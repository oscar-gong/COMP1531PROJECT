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
    '''Tests workspace reset'''
    #Reset everthing make sure the work space is clean
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

def test_initialisation():
    '''Tests initialisation'''
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

#channels.py
def test_channel_invite():
    '''Tests channel invite'''

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
    #User1 invites user 2
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "u_id":1
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/invite", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

def test_channel_details():
    '''Tests channel details'''
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1, 'channel_id':0
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{query_string}")
    payload = json.load(response)
    expected = {
        "name" : "channel1",
        "owner_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''}],
        "all_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''},
                         {'name_first': 'Sam', 'name_last': 'Blake', 'u_id': 1, 'profile_img_url': ''}]
    }
    assert payload == expected

def test_channel_messages():
    '''Tests channel messages'''
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1, 'channel_id':0, 'start':0
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messages?{query_string}")
    payload = json.load(response)
    expected = {'messages':[], 'start':0, 'end':-1}
    assert payload == expected

def test_channel_leave():
    '''Tests channel leave'''
    #User1 creates a channel
    value = {
        "token":USER_TOKEN_2,
        "channel_id":0
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/leave", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1, 'channel_id':0
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{query_string}")
    payload = json.load(response)
    expected = {
        "name" : "channel1",
        "owner_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''}],
        "all_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''}]
    }
    assert payload == expected

def test_channel_join():
    '''Tests channel join'''
    value = {
        "token":USER_TOKEN_2,
        "channel_id":0
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/join", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1, 'channel_id':0
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{query_string}")
    payload = json.load(response)
    expected = {
        "name" : "channel1",
        "owner_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''}],
        "all_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''},
                         {'name_first': 'Sam', 'name_last': 'Blake', 'u_id': 1, 'profile_img_url': ''}]
    }
    assert payload == expected

def test_channel_addowner():
    '''Tests channel addowner'''
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "u_id":1
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/addowner", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1, 'channel_id':0
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{query_string}")
    payload = json.load(response)
    expected = {
        "name" : "channel1",
        "owner_members" :   [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''},
                             {'name_first': 'Sam', 'name_last': 'Blake', 'u_id': 1, 'profile_img_url': ''}],
        "all_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''},
                         {'name_first': 'Sam', 'name_last': 'Blake', 'u_id': 1, 'profile_img_url': ''}]
    }
    assert payload == expected

def test_channel_removeowner():
    '''Tests channel removeowner'''
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "u_id":1
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1, 'channel_id':0
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details?{query_string}")
    payload = json.load(response)
    expected = {
        "name" : "channel1",
        "owner_members" :   [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''}],
        "all_members" : [{'name_first': 'Hayden', 'name_last': 'Jacobs', 'u_id': 0, 'profile_img_url': ''},
                         {'name_first': 'Sam', 'name_last': 'Blake', 'u_id': 1, 'profile_img_url': ''}]
    }
    assert payload == expected
    value = {
        "token":USER_TOKEN_1,
        "channel_id":0,
        "u_id":1
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/channel/removeowner", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

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
    '''Reset everthing make sure the work space is clean'''
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

def test_initialisation():
    '''Test initialisation '''
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

def test_user_profile():
    '''Tests user profile'''
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1,
        'u_id':USER_UID_1
    })
    response = urllib.request.urlopen(f"{BASE_URL}/user/profile?{query_string}")
    payload = json.load(response)
    assert payload['user']['u_id'] == USER_UID_1
    assert payload['user']['email'] == user1['email']
    assert payload['user']['name_first'] == user1['name_first']
    assert payload['user']['name_last'] == user1['name_last']
    assert payload['user']['handle_str'] is not None

    #Error checking

    #Not a valid user
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1,
        'u_id':-1000
    })
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(f"{BASE_URL}/user/profile?{query_string}")


def test_user_profile_setname():
    '''Tests user profile setname'''
    #User1 sets his name
    value = {
        "token":USER_TOKEN_1,
        "name_first":'kool',
        "name_last":'kids'
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setname", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #verify
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1,
        'u_id':USER_UID_1
    })
    response = urllib.request.urlopen(f"{BASE_URL}/user/profile?{query_string}")
    payload = json.load(response)
    assert payload['user']['u_id'] == USER_UID_1
    assert payload['user']['email'] == user1['email']
    assert payload['user']['name_first'] == 'kool'
    assert payload['user']['name_last'] == 'kids'
    assert payload['user']['handle_str'] is not None

    #Error checking


    #name_first is too long
    value = {
        "token":USER_TOKEN_1,
        "name_first":'kool'*1000,
        "name_last":'kidssss'
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setname", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(req)

    #name_last is too long

    value = {
        "token":USER_TOKEN_1,
        "name_first":'koollll',
        "name_last":'kidssss'*2000
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setname", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(req)

def test_user_profile_setemail():
    '''Tests user profile setemail'''
    #User1 sets his email
    #User1 has already changed its first name and last name
    value = {
        "token":USER_TOKEN_1,
        "email":'changed@gmail.com'
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setemail", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

    #Error checking

    #Invalid email
    value = {
        "token":USER_TOKEN_1,
        "email":'invalid_email'
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setemail", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(req)

    #Email has been taken
    value = {
        "token":USER_TOKEN_1,
        "email":user2['email']
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/setemail", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(req)

def test_user_profile_sethandle():
    '''Tests user profile sethandle'''
    #User1 sets his email
    #User1 has already changed its first name and last name
    value = {
        "token":USER_TOKEN_1,
        "handle_str":'lowercase'
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/sethandle", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}


    #verify
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1,
        'u_id':USER_UID_1
    })
    response = urllib.request.urlopen(f"{BASE_URL}/user/profile?{query_string}")
    payload = json.load(response)
    assert payload['user']['u_id'] == USER_UID_1
    assert payload['user']['email'] == 'changed@gmail.com'
    assert payload['user']['name_first'] == 'kool'
    assert payload['user']['name_last'] == 'kids'
    assert payload['user']['handle_str'] == 'lowercase'

    #Error checking

    #handle is too long
    value = {
        "token":USER_TOKEN_1,
        "handle_str":'lowercase'*20
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/sethandle", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(req)

    #handle has been taken
    value = {
        "token":USER_TOKEN_2,
        "handle_str":'lowercase'
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/user/profile/sethandle", data, CUSTOM_HEADER, method='PUT') # pylint: disable=line-too-long
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(req)


def test_user_all():
    '''Tests user all'''
    #verify
    query_string = urllib.parse.urlencode({
        'token': USER_TOKEN_1
    })
    response = urllib.request.urlopen(f"{BASE_URL}/users/all?{query_string}")
    payload = json.load(response)
    user = payload['users']
    assert len(user) == 3
    #u_id, email, name_first, name_last, handle_str
    #user1
    assert user[0]['u_id'] == USER_UID_1
    assert user[0]['email'] == 'changed@gmail.com'
    assert user[0]['name_first'] == 'kool'
    assert user[0]['name_last'] == 'kids'
    assert user[0]['handle_str'] == 'lowercase'
    #user2
    assert user[1]['u_id'] == USER_UID_2
    assert user[1]['email'] == user2['email']
    assert user[1]['name_first'] == user2['name_first']
    assert user[1]['name_last'] == user2['name_last']
    assert user[1]['handle_str'] == user2['name_first'].lower()+user2['name_last'].lower()
    #user3
    assert user[2]['u_id'] == USER_UID_3
    assert user[2]['email'] == user3['email']
    assert user[2]['name_first'] == user3['name_first']
    assert user[2]['name_last'] == user3['name_last']
    assert user[2]['handle_str'] == user3['name_first'].lower()+user3['name_last'].lower()

    #Error checking
    #verify
    query_string = urllib.parse.urlencode({
        'token': "invalid_token"
    })
    with pytest.raises(urllib.error.HTTPError):
        response = urllib.request.urlopen(f"{BASE_URL}/users/all?{query_string}")

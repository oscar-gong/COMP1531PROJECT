"""This module is designed for the system_test"""
import json
import urllib
# flask needed for urllib.parse
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
    '''Tests workplace reset'''
    #Reset everthing make sure the work space is clean
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

#auth.py
def test_auth_register():
    '''Tests auth register'''
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

    #Error checking

    #Invalid email
    value = {
        "email":'Invalid email',
        "password":user3['password'],
        "name_first":user3['name_first'],
        "name_last":user3['name_last']
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Email has already been used
    value = {
        "email":user3['email'],
        "password":user3['password'],
        "name_first":user3['name_first'],
        "name_last":user3['name_last']
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Poor password
    value = {
        "email":'test@gmail.com',
        "password":'POOR',
        "name_first":user3['name_first'],
        "name_last":user3['name_last']
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #First name is too long
    value = {
        "email":'test@gmail.com',
        "password":user3['password'],
        "name_first":'a'*100,
        "name_last":user3['name_last']
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Last name is too long
    value = {
        "email":'test@gmail.com',
        "password":user3['password'],
        "name_first":user3['name_first'],
        "name_last":'a'*100
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/register", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

def test_auth_logout():
    '''Tests auth logout'''
    #Logout user1
    value = {
        "token":USER_TOKEN_1
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['is_success']

    #Logout user2
    value = {
        "token":USER_TOKEN_2
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['is_success']

    #Logout user3
    value = {
        "token":USER_TOKEN_3
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['is_success']

    #Can not logout twice
    value = {
        "token":USER_TOKEN_3
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/logout", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response['is_success'] is False

def test_auth_login():
    '''Tests auth login'''
    global USER_TOKEN_1, USER_TOKEN_2, USER_TOKEN_3 # pylint: disable=global-statement
    #Login user1
    value = {
        "email":user1['email'],
        "password":user1['password'],
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/login", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)

    USER_TOKEN_1 = json_response['token']
    assert USER_UID_1 == 0
    assert USER_TOKEN_1 is not None

    #Login user2
    value = {
        "email":user2['email'],
        "password":user2['password'],
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/login", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)

    USER_TOKEN_2 = json_response['token']
    assert USER_UID_2 == 1
    assert USER_TOKEN_2 is not None

    #Login user3
    value = {
        "email":user3['email'],
        "password":user3['password'],
    }
    data = json.dumps(value).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/auth/login", data, CUSTOM_HEADER, method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)

    USER_TOKEN_3 = json_response['token']
    assert USER_UID_3 == 2
    assert USER_TOKEN_3 is not None

    #Error checking

    #Invalid email
    value = {
        "email":'Invalid email',
        "password":user3['password'],
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Wrong email (does not belong to the user)
    value = {
        "email":user1['email'],
        "password":user3['password'],
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

    #Wrong password (does not belong to the user)
    value = {
        "email":user1['email'],
        "password":user3['password'],
    }
    data = json.dumps(value).encode('utf-8')
    req = urllib.request.Request(f"{BASE_URL}/auth/login", data, CUSTOM_HEADER, method='POST')
    with pytest.raises(urllib.error.HTTPError):
        urllib.request.urlopen(req)

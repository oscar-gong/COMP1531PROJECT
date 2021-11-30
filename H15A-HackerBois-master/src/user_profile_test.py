'''This module tests user profile'''
import pytest
from user import user_profile
from user import user_profile_sethandle
from auth import auth_login
from auth import auth_register
from error import InputError, AccessError
from database import database
from projectDefines import user1, user2

#Tests that using clicking on own profile page will return the user and the correct information
def test_valid_user():
    '''Tests valid user'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    profile = user_profile(user['token'], user['u_id'])
    user_profile_sethandle(user['token'], 'hjacobs')
    assert profile is not None
    assert profile['user']['email'] == user1['email']
    assert profile['user']['name_first'] == 'Hayden'
    assert profile['user']['name_last'] == 'Jacobs'
    assert profile['user']['handle_str'] == 'haydenjacobs'

#Test shows a user logging in and generating a token but has an invalid U_id
#Error raise should be an InputError
def test_invalid_uid():
    '''Tests invalid user id'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    invalid_uid = -10
    with pytest.raises(InputError):
        user_profile(user['token'], invalid_uid)
#Logged into your account with a valid token and u_id but looking at other people's profile
#should show the other party's correct information
def test_other_profile():
    '''Tests other profile'''
    database.reset()
    auth_register("z6346463@ad.unsw.edu.au", "Password1234", "Jeremy", "Cutter")
    user_a = auth_login("z6346463@ad.unsw.edu.au", "Password1234")
    auth_register(user2['email'], user2['password'], user2['name_first'], user2['name_last'])
    user_b = auth_login(user2['email'], user2['password'])
    user_profile_sethandle(user_b['token'], 'sblake')

    profile_b = user_profile(user_a['token'], user_b['u_id'])
    assert profile_b is not None
    assert profile_b['user']['email'] == user2['email']
    assert profile_b['user']['name_first'] == 'Sam'
    assert profile_b['user']['name_last'] == 'Blake'
    assert profile_b['user']['handle_str'] == 'sblake'

def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    with pytest.raises(AccessError):
        user_profile('invalid_token', user['u_id'])

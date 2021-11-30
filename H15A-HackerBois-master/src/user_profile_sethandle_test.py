'''This module tests userprofile sethandle'''
import pytest
from user import user_profile
from user import user_profile_sethandle
from auth import auth_login
from auth import auth_register
from error import InputError
from database import database
from projectDefines import user1


# Create a new user using projectDefines
def new_user():
    '''Creates new user'''
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    user_profile_sethandle(user['token'], 'hjacobs')
    return user


# Assuming that the function has a checker that checks for invalid handles
# and if the hadles has been used before or not
def test_valid_handle():
    '''Tests valid handle'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['handle_str'] == 'hjacobs'
    new_handle = "jacobs123"
    user_profile_sethandle(user['token'], new_handle)
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['handle_str'] == 'jacobs123'
    auth_register("z6346463@ad.unsw.edu.au", "Password1234", "Jeremy", "Cutter")
    user2 = auth_login("z6346463@ad.unsw.edu.au", "Password1234")
    profile = user_profile(user2['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['handle_str'] == 'jacobs123'

# Check that error raised for invalid handle is InputError
# Check for handle for lower than 2 characters
def test_invalid_handle_1():
    '''Tests invalid handle'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['handle_str'] == 'hjacobs'
    new_handle = "h"
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], new_handle)

# Check new handle for blank
def test_invalid_handle_2():
    '''Tests invalid handle'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['handle_str'] == 'hjacobs'
    new_handle = ""
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], new_handle)

# Check new handele for more than 20 characters
def test_invalid_handle_3():
    '''Tests invalid handle'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['handle_str'] == 'hjacobs'
    new_handle = "abcdefghijklmnopqrstuvwxyz"
    with pytest.raises(InputError):
        user_profile_sethandle(user['token'], new_handle)
# Assume that the function has a checker to check for users handle and test if
# it has been used before or not, if not raised an InputError
def test_used_handle():
    '''Tests used handle'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['handle_str'] == 'hjacobs'
    auth_register("z6346463@ad.unsw.edu.au", "Password1234", "Jeremy", "Cutter")
    user2 = auth_login("z6346463@ad.unsw.edu.au", "Password1234")

    with pytest.raises(InputError):
        user_profile_sethandle(user2['token'], 'hjacobs')

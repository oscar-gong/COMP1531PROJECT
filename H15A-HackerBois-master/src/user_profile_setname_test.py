'''This module tests userprofile setname'''
import pytest
from user import user_profile
from user import user_profile_setname
from auth import auth_login
from auth import auth_register
from error import InputError
from database import database
from projectDefines import user1

def new_user():
    '''Creates new user'''
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])

    return user

#Testing if the user can change his first and last name and also if it changes in the system
#Allowing both user and others to see his updated names
def test_valid_name():
    '''Tests valid name'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['name_first'] == 'Hayden'
    assert profile['user']['name_last'] == 'Jacobs'

    user_profile_setname(user['token'], "Harry", "Potter")
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['name_first'] == 'Harry'
    assert profile['user']['name_last'] == 'Potter'

    auth_register("z6346463@ad.unsw.edu.au", "Password1234", "Jeremy", "Cutter")
    user2 = auth_login("z6346463@ad.unsw.edu.au", "Password1234")
    profile2 = user_profile(user2['token'], user['u_id'])
    assert profile2 is not None
    assert profile2['user']['name_first'] == 'Harry'
    assert profile2['user']['name_last'] == 'Potter'


# test that the user can't update his first_name with more than 50 characters
def test_invalid_first_name():
    '''Tests invalid first name'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['name_first'] == 'Hayden'
    assert profile['user']['name_last'] == 'Jacobs'

    invalid_name = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    with pytest.raises(InputError):
        user_profile_setname(user['token'], invalid_name, "Granger")

# test that the user can't update his last_name with more than 50 characters
def test_invalid_last_name():
    '''Tests invalid last name'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['name_first'] == 'Hayden'
    assert profile['user']['name_last'] == 'Jacobs'

    invalid_name = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
    with pytest.raises(InputError):
        user_profile_setname(user['token'], "Hermione", invalid_name)

# tests that the user can't update his first_name with less than 1 character
def test_blank_first_name():
    '''Tests blank first name'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['name_first'] == 'Hayden'
    assert profile['user']['name_last'] == 'Jacobs'

    with pytest.raises(InputError):
        user_profile_setname(user['token'], '', 'Weasley')

# tests that the user can't update his last_name with less than 1 character
def test_blank_last_name():
    '''Tests blank last name'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['name_first'] == 'Hayden'
    assert profile['user']['name_last'] == 'Jacobs'

    with pytest.raises(InputError):
        user_profile_setname(user['token'], 'Ron', '')

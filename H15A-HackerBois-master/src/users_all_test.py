'''This module tests user all'''
import pytest
from other import users_all
from auth import auth_login
from auth import auth_register
from projectDefines import user1
from database import database
from error import AccessError

# Check to see if user can see what is in the list
# Check to see if the list is correct by checking if he is inside
def test_valid_token():
    '''Tests valid token'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])
    group = users_all(user['token'])
    assert group is not None
    checker = False

    for users in group['users']:
        if users['u_id'] == user['u_id']:
            checker = True
    assert checker

#Check that all users can see everyone, that they all see the same list
def test_new_user():
    '''Tests new user'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_a = auth_login(user1['email'], user1['password'])
    auth_register("z6346463@ad.unsw.edu.au", "Password1234", "Jeremy", "Cutter")
    user_b = auth_login("z6346463@ad.unsw.edu.au", "Password1234")

    user_a_group = users_all(user_a['token'])
    user_b_group = users_all(user_b['token'])

    assert user_a_group == user_b_group

def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    auth_login(user1['email'], user1['password'])

    with pytest.raises(AccessError):
        users_all('invalid_token')

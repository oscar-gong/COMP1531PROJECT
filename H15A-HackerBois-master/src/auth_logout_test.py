'''This module tests auth logout'''
from database import database
from auth import auth_logout
from projectDefines import user1
from pytestHelperFunctions import create_login_user

def test_valid_token():
    '''Tests valid token'''
    database.reset()
    test_user = create_login_user(user1)
    assert auth_logout(test_user["token"])["is_success"]

def test_invalid_token_1():
    '''Tests invalid token'''
    database.reset()
    test_user = create_login_user(user1)
    #Logout once so the token becomes invalidated
    auth_logout(test_user["token"])
    #This should now return false as the token has been invalidated
    assert not auth_logout(test_user["token"])["is_success"]

def test_invalid_token_2():
    '''Tests invalid token'''
    database.reset()
    assert not auth_logout("notAToken")["is_success"]

def test_no_input():
    '''Tests no input'''
    database.reset()
    assert not auth_logout("")["is_success"]

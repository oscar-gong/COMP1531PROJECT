'''This module tests auth login'''
import pytest
from database import database
from auth import auth_login, auth_logout
from error import InputError
from projectDefines import user1
from pytestHelperFunctions import create_user


def test_valid_email():
    '''Tests valid email'''
    database.reset()
    test_user1 = create_user(user1)
    auth_login(test_user1["email"], test_user1["password"])


def test_invalid_email_1():
    '''Tests invalid email'''
    database.reset()
    with pytest.raises(InputError):
        auth_login("notAnEmailAtgmaildotcom", "password")

def test_invalid_email_2():
    '''Tests invalid email'''
    database.reset()
    with pytest.raises(InputError):
        auth_login("notAnEmailAtgmail.com", "password")

def test_no_email():
    '''Tests no email'''
    database.reset()
    with pytest.raises(InputError):
        auth_login("", "noUsername")

def test_no_password():
    '''Tests no password'''
    database.reset()
    with pytest.raises(InputError):
        auth_login("noPassword@gmail.com", "")

def test_wrong_password():
    '''Tests wrong password'''
    database.reset()
    test_user1 = create_user(user1)
    with pytest.raises(InputError):
        auth_login(test_user1["email"], test_user1["password"] * 2)

def test_wrong_email():
    '''Tests wrong email'''
    database.reset()
    with pytest.raises(InputError):
        auth_login("haveNotSignedUp@gmail.com", "RandomPassword")

def test_correct_output_size():
    '''Tests output size'''
    database.reset()
    test_user1 = create_user(user1)
    assert len(auth_login(test_user1["email"], test_user1["password"])) == 2

#Test that users u_id doesn't change between registering and login
#And that between different sessions u_id doesn't change but token changes
def test_repeated_login():
    '''Tests repeated login'''
    database.reset()
    test_user1 = create_user(user1)
    user = auth_login(test_user1["email"], test_user1["password"])
    auth_logout(user['token'])

    same_user = auth_login(test_user1["email"], test_user1['password'])
    assert test_user1['u_id'] == user['u_id']
    assert user['u_id'] == same_user['u_id']
    assert user['token'] != same_user['token']

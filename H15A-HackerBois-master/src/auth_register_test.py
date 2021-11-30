'''This module tests auth register'''
import pytest
from database import database
from auth import auth_register
from error import InputError
from user import user_profile

def test_valid_register():
    '''Tests valid register'''
    database.reset()
    auth_register("goodEmail@gmail.com", "goodPassword1", "Silly", "Jimmy")

def test_same_handlestr():
    '''Tests same handle'''
    database.reset()
    #user1 with handle sillyjimmy
    auth_register("goodEmail@gmail.com", "goodPassword1", "Silly", "Jimmy")

    #User2 with handle sillyjimmy1
    user2 = auth_register("betterEmail@gmail.com", "betterPassword1", "Silly", "Jimmy")
    user2_detail = user_profile(user2['token'], user2['u_id'])
    assert user2_detail['user']['handle_str'] == 'sillyjimmy0'

def test_invalid_email():
    '''Tests invalid email'''
    database.reset()
    with pytest.raises(InputError):
        auth_register("notAnEmailAtGeeMailDotCom", "goodPassword1", "Silly", "Jimmy")

def test_used_email():
    '''Tests used email'''
    database.reset()
    #New email
    auth_register("goodEmail@gmail.com", "goodPassword1", "Silly", "Jimmy")
    #Email has been taken
    with pytest.raises(InputError):
        auth_register("goodEmail@gmail.com", "goodPassword1", "Silly", "Jimmy")

def test_invalid_password():
    '''Tests invalid password'''
    database.reset()
    with pytest.raises(InputError):
        auth_register("goodEmail@gmail.com", "bad", "Silly", "Jimmy")

def test_invalid_first_name_1():
    '''Tests invalid first name'''
    database.reset()
    #Name is too short
    with pytest.raises(InputError):
        auth_register("goodEmail@gmail.com", "goodPassword1", "", "Jimmy")

def test_invalid_first_name_2():
    '''Tests invalid first name'''
    database.reset()
    #Name is too long
    invalid_name = "a" * 51

    with pytest.raises(InputError):
        auth_register("goodEmail@gmail.com", "goodPassword1", invalid_name, "Jimmy")

def test_invalid_last_name_1():
    '''Tests invalid last name'''
    database.reset()
    #Name is too short
    with pytest.raises(InputError):
        auth_register("goodEmail@gmail.com", "goodPassword1", "Silly", "")

def test_invalid_last_name_2():
    '''Tests invalid last name'''
    database.reset()
    #Name is too long
    invalid_name = "a" * 51

    with pytest.raises(InputError):
        auth_register("goodEmail@gmail.com", "goodPassword1", "Silly", invalid_name)

#Test function that u_id starts at 0 for first user and every user is incremented by 1
#Test that token is different for each user
def test_no_repeated_uid_and_token():
    '''Tests no repeated user id and toekn'''
    database.reset()
    user_a = auth_register("goodEmail@gmail.com", "goodPassword1", "Silly", "Jimmy")
    user_b = auth_register("goodDay@gmail.com", "goodPassword2", "Silly", "Billy")
    assert user_a['u_id'] == 0
    assert user_b['u_id'] == user_a['u_id'] + 1
    assert user_a['token'] != user_b['token']

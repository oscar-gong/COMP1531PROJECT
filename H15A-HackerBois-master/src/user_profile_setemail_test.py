'''This module tests userprofile setemail'''
import pytest
from user import user_profile
from user import user_profile_setemail
from auth import auth_login
from auth import auth_register
from error import InputError
from database import database
from projectDefines import user1

# Create a new user using projectDefines
def new_user():
    '''creates new user'''
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])

    return user


# Assume that the function user_profile_setemail has a checker to test if
# it's a valid / used email but for now valid_email_check to make the email fail
# Check to see if the updated email can be seen by both self and other people
def test_valid_email():
    '''Tests valid email'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == user1['email']

    new_email = "HelloWorld@gmail.com"
    user_profile_setemail(user['token'], new_email)

    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == new_email

    auth_register("z6346463@ad.unsw.edu.au", "Password1234", "Jeremy", "Cutter")
    user2 = auth_login("z6346463@ad.unsw.edu.au", "Password1234")
    profile = user_profile(user2['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == new_email


#test for cases of invalid email using the valid_email_checker_function
def test_invalid_email_1():
    '''Tests invalid email'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == user1['email']

    new_email = "Invalidemailatgmail.com"
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], new_email)

#Invalid email_2
def test_invalid_email_2():
    '''Tests invalid email'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == user1['email']
    new_email = "@gmail.com"
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], new_email)

#Invalid email_3
def test_invalid_email_3():
    '''Tests invalid email'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == user1['email']

    new_email = "Invalidemail@"
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], new_email)

#Invalid email_4
def test_invalid_email_4():
    '''Tests invalid email'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == user1['email']

    new_email = "Invalidemail@gmail"
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], new_email)

# Assuming that the function has a valid email checker and a used email checker
# test if email is valid and if it is, test if it's been used
def test_used_email():
    '''Tests used email'''
    database.reset()
    user = new_user()
    profile = user_profile(user['token'], user['u_id'])
    assert profile is not None
    assert profile['user']['email'] == user1['email']
    auth_register("z6346463@ad.unsw.edu.au", "Password1234", "Jeremy", "Cutter")
    new_email = user1['email']
    with pytest.raises(InputError):
        user_profile_setemail(user['token'], new_email)

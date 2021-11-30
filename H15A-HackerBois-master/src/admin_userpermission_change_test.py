'''This module tests admin user permission change'''
import pytest
from auth import auth_register, auth_login
from admin import admin_userpermission_change
from channel import channel_join
from channels import channels_create
from error import AccessError, InputError
from projectDefines import user1, user2
from database import database

def new_user(email, password, name_first, name_last):
    '''Creates new user'''
    auth_register(email, password, name_first, name_last)
    user_data = auth_login(email, password)

    return user_data

def test_valid():
    '''Tests valid user'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    owner = database.get_user_object(user_a['token'])
    member = database.get_user_object(user_b['token'])

    assert owner.permission_id == 1
    assert member.permission_id == 2

    channel_id = channels_create(user_a['token'], 'Test Channel', True)['channel_id']
    channel_join(user_b['token'], channel_id)
    channel = database.get_channel_by_id(channel_id)

    admin_userpermission_change(user_a['token'], user_b['u_id'], 1)
    assert member.permission_id == 1
    assert channel.is_owner(member)
    admin_userpermission_change(user_b['token'], user_a['u_id'], 2)
    assert owner.permission_id == 2


def test_invalid_token():
    '''Tests invalid token'''
    database.reset()
    #Get new user
    user_a_token = "Invalid_token"
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    with pytest.raises(AccessError):
        admin_userpermission_change(user_a_token, user_b['u_id'], 1)

def test_invalid_u_id():
    '''Tests invalid user id'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b_uid = -1

    with pytest.raises(InputError):
        admin_userpermission_change(user_a['token'], user_b_uid, 1)

def test_not_owner():
    '''Tests user not owner'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    with pytest.raises(AccessError):
        admin_userpermission_change(user_b['token'], user_a['u_id'], 1)

def test_invalid_permission_id():
    '''Tests invalid permission id'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    with pytest.raises(InputError):
        admin_userpermission_change(user_a['token'], user_b['u_id'], -1)

def test_removing_only_owner():
    '''Tests removing only owner'''
    database.reset()
    #Get new user
    user_a = new_user(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user_b = new_user(user2['email'], user2['password'], user2['name_first'], user2['name_last'])

    owner = database.get_user_object(user_a['token'])
    member = database.get_user_object(user_b['token'])

    assert owner.permission_id == 1
    assert member.permission_id == 2

    with pytest.raises(InputError):
        admin_userpermission_change(user_a['token'], user_a['u_id'], 2)

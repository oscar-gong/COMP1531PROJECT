'''This module implements admin user permission change'''
from error import InputError, AccessError
from database import database

#Check if user is owner by calling token and checking permission_id == 1
#Check if user to be change by calling user_id is real
#Check that permission_id is only either 1 or 2
#Change permissions
def admin_userpermission_change(token, u_id, permission_id):
    '''Changes permission of admin'''
    owner = database.get_user_object(token)
    user = database.get_user_object_by_id(u_id)

    if owner == "NOT_FOUND":
        raise AccessError(description="Invalid Token")
    elif owner.permission_id != 1:
        raise AccessError(description="User is not allowed to change user permissions")
    elif user == "NOT_FOUND":
        raise InputError(description="User not Found")
    elif (permission_id < 1 or permission_id > 2):
        raise InputError(description="Permission ID is not allowed")
    else:
        if len(database.get_owner_list()) == 1 and permission_id == 2:
            if owner == user:
                raise InputError("Error doing this will result in slackr not having an Owner")

        user.set_permission_id(permission_id)
        channel_list = database.user_channel_list(u_id)

        for channel in channel_list:
            if not channel.is_owner(user):
                channel.add_owner(user)

    return {}

def admin_user_remove(token, u_id):
    '''Gives Admin the right to remove Users'''
    owner = database.get_user_object(token)
    user = database.get_user_object_by_id(u_id)

    if owner == "NOT_FOUND":
        raise AccessError(description="Invalid Token")
    elif owner.permission_id != 1:
        raise AccessError(description="User does not have permission to remove user")
    elif user == "NOT_FOUND":
        raise InputError(description="User not Found")
    else:
        if len(database.get_owner_list()) == 1:
            if owner == user:
                raise InputError("Error doing this will result in slackr not having an Owner")

        database.remove_user(user)
        channel_list = database.user_channel_list(u_id)
        for channel in channel_list:
            channel.remove_user_messages_by_u_id(u_id)
            channel.remove_user_reacts_by_u_id(u_id)
            channel.remove_member(user)


    return {}

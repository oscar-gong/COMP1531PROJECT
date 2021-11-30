"""This module contains al the functions required for manipulating numerous channels"""
from database import database, ChannelObject
from error import InputError, AccessError

def channels_create(token, name, is_public):
    """Creates a new channel with that name that is either a public or private channel.
    Takes in a valid token and a new name and an is_public parameter.
    """
    if len(name) > 20:
        raise InputError(description='Name is more than 20 characters long')
    user = database.get_user_object(token)
    if user == "NOT_FOUND":
        raise AccessError(description='Invalid token , user is unfound')
    if check_name_exist(name):
        raise InputError(description='Channel name is already existed')

    #Get the last channel_id which has been created then + 1
    #Return that channel_id
    channel_id = database.get_last_channel_id()

    #Create ChannelObject class
    #Create a new channel with the given details
    new_channel = ChannelObject(user, name, is_public, channel_id)

    #Add the user to the list of all members and owner
    new_channel.add_owner(user)
    new_channel.add_member(user)

    #Add the new channel to the channel list in the database
    database.add_channel_to_list(new_channel)

    #Increment the last channel ID
    database.update_last_channel_id()

    return {"channel_id":channel_id}


def channels_list(token):
    """Provide a list of all channels that the authorised user is part of when given a valid token"""

    #If user not found just return None
    if database.get_user_object(token) == "NOT_FOUND":
        return None

    channel_list = {"channels":[]}
    user = database.get_user_object(token)
    for channel in database.channels['channels']:
        if channel.member_in_channel(user.u_id):
            channel_list['channels'].append(channel.channel_details())
    return channel_list


def channels_listall(token):
    """Provide a list of all channels on the server given an active token"""
    if database.get_user_object(token) == "NOT_FOUND":
        raise AccessError(description='User is not found')
    channel_list = {"channels":[]}

    for channel in database.channels['channels']:
        channel_list['channels'].append(channel.channel_details())
    return channel_list

def check_name_exist(name):
    """Check if the given channel name already exists in the channel list"""
    for channel in database.channels['channels']:
        if channel.name == name:
            return True
    return False

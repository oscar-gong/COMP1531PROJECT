# pylint: disable=C0111
"""
This module contains all the functions relating to within a channel. For creating channels
and other functions, check the channels module
"""
from database import database
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    '''
    Given a valid token, valid channel_id and a users u_id,
    invite the user with the given u_id into the channel
    '''
    if not database.is_in_channel(channel_id):
        raise InputError(description="Invalid Channel ID") # When the channel ID is invalid
    user = database.get_user_object(token)
    channel = database.get_channel_by_id(channel_id)
    if not channel.member_in_channel(user.u_id):
        # When the authorised user is not a member of the channel
        raise AccessError(description="User does not have permission")
    user_to_be_invited = database.get_user_object_by_id(u_id)
    if user_to_be_invited == "NOT_FOUND":
        #When u_id does not refer to a valid user
        raise InputError(description="Invited User does not exist")
    if not channel.member_in_channel(user_to_be_invited.u_id):
        channel.add_member(user_to_be_invited) # Add member to the all_members list in the channel
        if user_to_be_invited in database.get_owner_list():
            channel.add_owner(user_to_be_invited)
    return {}

def channel_details(token, channel_id):
    '''Given an active token and a valid channel_id, return the channel name,
    owners of the channel, and all the members of the channel'''
    if not database.is_in_channel(channel_id):
        raise InputError(description='Invalid channel id') # When the channel ID is invalid
    user = database.get_user_object(token)
    channel = database.get_channel_by_id(channel_id)
    if not channel.member_in_channel(user.u_id):
        # When the authorised user is not a member of the channel
        raise AccessError(description='User is not a member of this group')
    dic = {'name':[], 'owner_members':[], 'all_members':[]}
    dic['name'] = channel.name
    dic['owner_members'] = channel.get_owner_detail_list()
    dic['all_members'] = channel.get_user_detail_list()
    return dic

def channel_messages(token, channel_id, start):
    '''Given an active token, a valid channel_id and a start index, returns the next 50 messages
    from that index
    '''
    if not database.is_in_channel(channel_id):
        raise InputError(description='Invalid channel id') # When the channel ID is invalid
    channel = database.get_channel_by_id(channel_id)
    if start > channel.get_number_of_messages():
        # When start is greater than the amount of messages
        raise InputError(description='Channel does not contain this many messages')
    user = database.get_user_object(token)
    if not channel.member_in_channel(user.u_id):
        # When the authorised user is not a member of the channel
        raise AccessError(description='User is not a member of the channel')
    dic = {'messages':[], 'start':[], 'end':[]}
    dic['start'] = start
    # If start + 50 is greater than the amount of messages in the channel,
    # Make end = -1
    # e.g. if the channel has 124 messages
    # start will be 0, 50, 100 and end will be 50, 100 and -1
    # 1 to 50, 51 to 100, 101 to 124 messages
    # 0 to 49, 50 to 99, 100 to 123 start
    if (start + 50) > channel.get_number_of_messages():
        dic['end'] = -1
    else:
        dic['end'] = start+50
    if dic['end'] == -1:
        for i in range(start, channel.get_number_of_messages()):
            dic['messages'].append(channel.messages[i].get_message(user.u_id))
    elif dic['end'] == start+50:
        for i in range(start, (start+50)):
            dic['messages'].append(channel.messages[i].get_message(user.u_id))

    return dic

def channel_leave(token, channel_id):
    '''Given a valid token and channel_id, remove the user with the given token from the channel'''
    if not database.is_in_channel(channel_id):
        raise InputError(description="Channel ID is not valid") # When the channel ID is invalid
    channel = database.get_channel_by_id(channel_id)
    user = database.get_user_object(token)
    if not channel.member_in_channel(user.u_id):
        # When the authorised user is not a member of the channel
        raise AccessError(description="User is not a member of the channel")
    channel.remove_member(user)
    if channel.all_members == []:
        database.channels['channels'].remove(channel)
    elif channel.owner_members == []:
        new_owner = channel.all_members[0]
        channel.add_owner(new_owner)
    return {}

def channel_join(token, channel_id):
    '''Given a valid token and channel_id, add the user with the given token to the channel'''
    if not database.is_in_channel(channel_id):
        raise InputError(description='Invalid channel id') # When the channel ID is invalid
    channel = database.get_channel_by_id(channel_id)
    if not channel.is_public:
        raise AccessError(description='This channel is private') # When the channel is not public
    user = database.get_user_object(token)
    channel.add_member(user)
    if user in database.get_owner_list():
        channel.add_owner(user)

    return {}

def channel_addowner(token, channel_id, u_id):
    '''Given a valid token and channel_id, set the user with the given u_id as an owner'''
    if not database.is_in_channel(channel_id):
        raise InputError(description="Channel ID is invalid") # When the channel ID is invalid
    channel = database.get_channel_by_id(channel_id)
    owner = database.get_user_object(token)
    user = database.get_user_object_by_id(u_id)
    if channel.is_owner(user):
        # When the target user is already an owner of the channel
        raise InputError(description="Invited user is already an owner")
    if not channel.is_owner(owner) and not owner.u_id == 0:
        # When the user is not an owner of the channel or slackr
        raise AccessError(description="User is not an owner")
    channel.add_owner(user) # Add target user to the owner list in channel
    return {}

def channel_removeowner(token, channel_id, u_id):
    '''IGiven a valid token and channel_id, remove the user with the given u_id from being an owner'''
    if not database.is_in_channel(channel_id):
        raise InputError(description="Channel ID is invalid") # When the channel ID is invalid
    channel = database.get_channel_by_id(channel_id)
    owner = database.get_user_object(token)
    user = database.get_user_object_by_id(u_id)
    if not channel.is_owner(user):
        # When the target user is already not an owner
        raise InputError(description="User is not an owner")
    if not channel.is_owner(owner) and not owner.u_id == 0:
        # When the user is not an owner of the channel or slackr
        raise AccessError(description="User does not have permission")
    channel.remove_owner(user) # Remove the target user from the list of owners
    return {}

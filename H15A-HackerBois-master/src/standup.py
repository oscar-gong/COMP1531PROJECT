'''This module contains all the functions relating to standup'''
from datetime import datetime, timedelta, timezone
from database import database, MessageObject
from error import InputError, AccessError


def standup_start(token, channel_id, length):
    '''Given a valid token and valid channel id, start a standup
    for the given length'''
    channel = database.get_channel_by_id(channel_id)
    user = database.get_user_object(token)
    if channel is None:
        raise InputError(description="Channel does not exist")
    if channel.standup_info["active"]:
        raise InputError(description="Channel standup already active")

    #Set time_finish
    time_finish = datetime.utcnow() + timedelta(seconds=length)
    channel.standup_info["time_finish"] = time_finish.replace(tzinfo=timezone.utc).timestamp()
    #Set the user who started the standup
    channel.standup_info["start_user"] = user
    channel.standup_info["is_active"] = True
    channel.start_standup_timer(length)
    return {
        "time_finish" : time_finish.replace(tzinfo=timezone.utc).timestamp()
    }

def standup_active(token, channel_id):
    '''Given an acive token and valid channel_id, checks
    if the channel has a standup active'''
    channel = database.get_channel_by_id(channel_id)

    #Checks both channel and token is valid
    if channel is None or (database.get_user_object(token) == "NOT_FOUND"):
        raise InputError(description="channel or user does not exist")

    return {
        "is_active" : channel.standup_info["active"],
        "time_finish" : channel.standup_info["time_finish"]
    }

def standup_send(token, channel_id, message):
    '''Given a valid channel_id with an active standup
    send a message into it which is stored and displayed
    all at once after the standup ends'''
    channel = database.get_channel_by_id(channel_id)
    if len(message) > 1000:
        raise InputError(description="Message is too long")
    elif channel is None:
        raise InputError(description="Channel does not exist")
    elif not channel.standup_info["active"]:
        raise InputError(description="Standup is not active")
    elif not channel.member_in_channel(database.get_user_object(token).u_id):
        raise AccessError(description="Member is not in channel")

    message_id = database.get_last_message_id()

    m_object = MessageObject(database.get_user_object(token).u_id, message, message_id)
    channel.standup_queue.append(m_object)
    return {}

# pylint: disable=W0613,W0107,W0611,C0200
"""This module is the implementation of message.py"""
from datetime import datetime, timezone
import threading
import re
import os
import user
import hangman
from database import database, MessageObject, ReactObject, UserEntity
from error import InputError, AccessError
SERVER_PORT = 5052


def message_send(token, channel_id, message):
    '''Given an active token and valid channel id, send a message to the channel'''
    if len(message) > 1000:
        raise InputError(description='Message is more than 1000 characters')
    channel_send = database.get_channel_by_id(channel_id)
    if channel_send is None:
        raise AccessError(description='Not a valid channel')
    user_send = database.get_user_object(token)
    if user_send == "NOT_FOUND":
        raise AccessError(description='Not a valid user')
    user_send = user_send.get_user()
    if not channel_send.member_in_channel(user_send['u_id']):
        raise AccessError(description='You are not a member of this channel')

    #get message_id
    message_id = database.get_last_message_id()

    new_user = database.get_user_object_by_id(-1)
    if new_user == "NOT_FOUND":
        new_user = UserEntity(None, "None", "Hangman", "Bot", -1, None, 0)
        new_user.set_token(new_user.generate_token())
        database.registered_users.append(new_user)
        database.active_users[new_user.token] = new_user
        new_user.set_profile_image_url(f'http://localhost:{str(SERVER_PORT)}/imgurl/bot.jpg')

    if re.match("/hangman$", message):
        hangman_bot = new_user.get_user()
        test = (
            f"{user_send['name_first']} {user_send['name_last']} started Hangman!\n"
            f"{hangman.hangman_start(channel_id)}"
        )
        msg = MessageObject(hangman_bot['u_id'], test, message_id)
        channel_send.add_message_to_channel(msg)
        database.update_last_message_id()
        return {"message_id":message_id}

    if re.match("/guess [a-zA-Z]$", message):
        hangman_bot = new_user.get_user()
        test = (
            f"{user_send['name_first']} {user_send['name_last']} guessed {message[-1]}\n"
            f"{hangman.hangman_guess(channel_id, message[-1])}"
        )
        msg = MessageObject(hangman_bot['u_id'], test, message_id)
        channel_send.add_message_to_channel(msg)
        database.update_last_message_id()
        return {"message_id":message_id}
    #Create message object
    msg = MessageObject(user_send['u_id'], message, message_id)

    #Add the message object to channel
    channel_send.add_message_to_channel(msg)

    #Updat the message_id
    database.update_last_message_id()


    return {"message_id":message_id}

def message_remove(token, message_id):
    '''Given an active token and valid message id, remove it'''
    user_a = database.get_user_object(token)
    if user_a == "NOT_FOUND":
        raise AccessError(description='user is not found')
    channel = None #set channel = none first
    for chan in database.channels['channels']:
        if chan.contains_message(message_id):
            channel = chan # if message is found, set channel equal to the channel it is found in
            break
    if channel is None:
        # if no channels were found, channel should equal to none
        raise InputError(description='Channel is not found')
    message = channel.get_message_by_id(message_id) # get the message in the channel
    # if the user did not send the message, or the user is not an owner of the channel or,
    # the user is not an owner of slackr, raise AccessError
    if message.u_id != user_a.u_id and not channel.is_owner(user_a) and user_a.get_permission_id() != 1:
        raise AccessError(description='You are not permitted to remove the message!')
    channel.messages.remove(message) # Remove message
    return {}



def message_edit(token, message_id, message):
    '''Given a valid token, message id and new message, edit an existing message'''
    if not message:
        raise InputError(description='Given message is blank!')
    user_a = database.get_user_object(token)
    if user_a == "NOT_FOUND":
        raise AccessError(description='user is not found')
    channel = None #set channel = none first
    for chan in database.channels['channels']:
        if chan.contains_message(message_id):
            channel = chan # if message is found, set channel equal to the channel it is found in
            break
    if channel is None:
        # if no channels were found, channel should equal to none
        raise InputError(description='Channel is not found')
    message_ = channel.get_message_by_id(message_id) # get the message in the channel
    # if the user did not send the message, or the user is not an owner of the channel or,
    # the user is not an owner of slackr, raise AccessError
    if message_.u_id != user_a.u_id and not channel.is_owner(user_a) and user_a.get_permission_id() != 1:
        raise AccessError(description='You are not permitted to edit the message!')
    message_.edit_message(message) # Edit message

    return {}

def message_react(token, message_id, react_id):
    '''React a message with the given message_id and react_id'''
    user_a = database.get_user_object(token)
    message = database.get_message_object_by_id(message_id)
    channel = database.get_channel_by_message_id(message_id)
    valid_reacts = [1]

    if not channel.member_in_channel(user_a.u_id):
        raise InputError("message_id is not a valid message within the channel")
    if react_id not in valid_reacts:
        raise InputError("react_id is not a valid React ID.")
    react = None
    #Search to see if the current react_id already exists
    for reacts in message.reacts:
        if reacts.react_id == react_id:
            #set the current react to the react object
            react = reacts
            break
    #Create a new react object if not found
    if react is None:
        #an existing react for that object cant be found
        new_react = ReactObject(react_id, user_a.u_id)
        message.add_reacts_object(new_react)
    elif user_a.u_id in react.u_ids:
        raise InputError("User has already reacted on the message")
    else:
        react.u_ids.append(user_a.u_id)

    return {}

def message_unreact(token, message_id, react_id):
    '''Unreact a message with the given message_id and react_id'''
    user_a = database.get_user_object(token)
    message = database.get_message_object_by_id(message_id)
    channel = database.get_channel_by_message_id(message_id)
    valid_reacts = [1]
    if not channel.member_in_channel(user_a.u_id):
        raise InputError("message_id is not a valid message within the channel")
    if react_id not in valid_reacts:
        raise InputError("react_id is not a valid React ID.")
    react = None
    #Checks to see if the current react exists
    for reacts in message.reacts:
        if reacts.react_id == react_id:
            react = reacts
            break
    if react is None:
        raise InputError("user has not yet reacted on the message")
    if not user_a.u_id in react.u_ids:
        raise InputError("user has already unreacted on the message")
    #Remove the current user from react
    react.remove_user_from_reacts(user_a.u_id)

    return {}

def message_pin(token, message_id):
    '''Pin a message given a valid message id'''
    user_a = database.get_user_object(token)
    message_dict = database.get_message_by_id(message_id)
    channel = message_dict['channel']
    msg = message_dict['message']

    if user_a == "NOT_FOUND":
        raise AccessError(description="Invalid Token")

    if not channel.member_in_channel(user_a.u_id):
        raise AccessError(description="User is not a member of this Channel")
    elif not channel.is_owner(user_a) and user_a.get_permission_id != 1:
        raise InputError(description="User does not have permission")
    elif msg.is_pinned:
        raise InputError(description="Message is already pinned")
    channel.messages.remove(msg)
    channel.messages.insert(0, msg)
    channel.increment_pinned_count()
    msg.set_pinned()

    return {}

def message_unpin(token, message_id):
    '''Unpin a pinned message with the given message id'''
    user_a = database.get_user_object(token)
    message_dict = database.get_message_by_id(message_id)
    channel = message_dict['channel']
    msg = message_dict['message']

    if user_a == "NOT_FOUND":
        raise AccessError(description="Invalid Token")

    if not channel.member_in_channel(user_a.u_id):
        raise AccessError(description="User is not a member of this Channel")
    elif not channel.is_owner(user_a) and user_a.get_permission_id() != 1:
        raise InputError(description="User does not have permission")
    elif not msg.is_pinned:
        raise InputError(description="Message is already unpinned")
    channel.messages.remove(msg)
    channel.insert_message_by_id(msg)
    channel.decrement_pinned_count()
    msg.set_un_pinned()

    return {}

def message_sendlater(token, channel_id, message, time_sent):
    '''Send a message to a channel after a delayed time'''
    user_a = database.get_user_object(token)
    channel = database.get_channel_by_id(channel_id)
    interval = time_sent - datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()

    if user_a == "NOT_FOUND":
        raise AccessError(description="Invalid Token")
    elif channel is None:
        raise InputError(description="Invalid Channel ID")

    if not channel.member_in_channel(user_a.u_id):
        raise AccessError(description="You have not joined this Channel")
    elif len(message) > 1000:
        raise InputError(description="Message needs to be below 1000 characters")
    elif interval < 0:
        raise InputError(description="Time sent is in the past")

    #get message_id
    message_id = database.get_last_message_id()
    #Create message object
    msg = MessageObject(user_a.u_id, message, message_id)

    #Update the message_id
    database.update_last_message_id()
    threading.Timer(interval, channel.send_message_now, [msg]).start()

    return {"message_id":message_id}

'''This module implements other'''
import operator
from database import database
from channels import channels_list
from error import AccessError

def users_all(token):
    '''Get all registered users in the database'''
    if database.get_user_object(token) == "NOT_FOUND":
        raise AccessError(description='Invalid Token')
    else:
        return {"users":database.get_all_users()}

def search(token, query_str):
    '''Search for all msgs in channels that the user is part of that matches the query_str
    msgs should be a dic in a list sorted according to id'''
    messages = []
    curr_user = database.get_user_object(token)
    #Get list of channels that user is in returns a list of channel_details dictionary
    channel_list = channels_list(token)
    query_list = query_str.split(" ")

    for channels in channel_list['channels']:
        #Get the ChannelObject using database and channel id from the channel_details
        channel = database.get_channel_by_id(channels['channel_id'])
        for message in channel.messages:
            #Get the message dictionary using database and message_object
            #Search through messages to see if it matches at least one of the query words
            #then break once found also check query words should ignore cases
            msg = message.get_message(curr_user.u_id)

            for query in query_list:
                if query.lower() in msg['message'].lower():
                    matched_msg = msg
                    messages.append(matched_msg)
                    break
    #Sort messages from most recent to least recent
    messages.sort(key=operator.itemgetter('time_created'), reverse = True)

    return {'messages': messages}

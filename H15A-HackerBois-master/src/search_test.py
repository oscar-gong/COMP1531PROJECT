'''This module tests search'''
import time
from other import search
from auth import auth_login, auth_register
from message import message_send
from channels import channels_create
from database import database
from projectDefines import user1


# Create a new user using projectDefines
def new_user():
    '''Creates new user'''
    auth_register(user1['email'], user1['password'], user1['name_first'], user1['name_last'])
    user = auth_login(user1['email'], user1['password'])

    return user

#Test searching for a query that exists in the database
#checking to make sure that the msgs found actually contain the query searched
#checkting to see if query can be found ignoring cases
def test_search_term_positive():
    '''Tests search term positive'''
    database.reset()
    user = new_user()
    channel_id = channels_create(user['token'], "test", True)

    message_send(user['token'], channel_id['channel_id'], "Hello wOrld")
    time.sleep(1)
    message_send(user['token'], channel_id['channel_id'], "hello World 1")

    query = "Hello"
    msgs = search(user['token'], query)
    assert msgs is not None
    assert msgs['messages'][0]['message'] == "hello World 1"
    for i in msgs['messages']:
        assert query.lower() in i['message'].lower()

    query = "World"
    msgs = search(user['token'], query)
    assert msgs is not None
    assert msgs['messages'][0]['message'] == "hello World 1"
    for i in msgs['messages']:
        assert query.lower() in i['message'].lower()


# Test searching for a query that does not exist in the database
# or an invalid search term such as "space"
# function should return an empty list
def test_search_term_negative():
    '''Tests search term negative'''
    database.reset()
    user = new_user()

    channel_id = channels_create(user['token'], "test", True)

    message_send(user['token'], channel_id['channel_id'], "Hello world")

    query = "hhrj34hhgf"
    msgs = search(user['token'], query)
    assert msgs is not None
    assert msgs['messages'] == []

# Assumption that the search function will seperate the string by spaces and
# search for each word individually
# So even if only one of the word in the query matches there will still be a search result
def test_double_search_term():
    '''Tests double search term'''
    database.reset()
    user = new_user()
    channel_id = channels_create(user['token'], "test", True)

    message_send(user['token'], channel_id['channel_id'], "Hello world")

    query = "Hello someone"
    msgs = search(user['token'], query)
    checker = [x for x in range(len(msgs['messages']))]

    # Check that the search is working for two words and can find searches relevant to either words
    assert msgs is not None
    query_list = query.split(" ")
    for i in query_list:
        for jidx, j in enumerate(msgs['messages']):
            if i in j['message']:
                checker[jidx] = "Yes"

    # Check that all msgs found contains at least one of the relevant words
    for k in checker:
        assert k == "Yes"


    query = "large world"
    msgs = search(user['token'], query)
    checker = [x for x in range(len(msgs['messages']))]

    # Check that the search is working for two words and can find searches relevant to either words
    assert msgs is not None
    query_list = query.split(" ")
    for i in query_list:
        for jidx, j in enumerate(msgs['messages']):
            if i in j['message']:
                checker[jidx] = "Yes"

    # Check that all msgs found contains at least one of the relevant words
    for k in checker:
        assert k == "Yes"

'''This file contains useful urllib tests'''
#pylint: disable=C0103
import json
import sys
import urllib.request
import urllib.parse
import time # pylint: disable=unused-import
from database import database # pylint: disable=unused-import
from projectDefines import user1, user2 # pylint: disable=unused-import

BASE_URL = "http://127.0.0.1:5052"

def auth_register_http(user):
    '''auth register http'''
    #POST Request
    data = json.dumps({
        "email" : user["email"],
        "password" : user["password"],
        "name_first" : user["name_first"],
        "name_last" : user["name_last"]
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    user["u_id"] = payload["u_id"]
    user["token"] = payload["token"]
    return payload

def auth_login_http(user):
    '''auth login http'''
    #POST Request
    data = json.dumps({
        "email" : user["email"],
        "password" : user["password"]
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    user["u_id"] = payload["u_id"]
    user["token"] = payload["token"]
    return payload

def message_send_http(token, channel_id, message):
    '''message send http'''
    #POST
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "message" : message
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    return payload

def message_react(token, message_id, react_id):
    '''message react http'''
    #POST
    data = json.dumps({
        "token" : token,
        "message_id" : message_id,
        "react_id" : react_id
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/message/react",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    return payload

def message_unreact(token, message_id, react_id):
    '''message unreact http'''
    #POST
    data = json.dumps({
        "token" : token,
        "message_id" : message_id,
        "react_id" : react_id
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/message/unreact",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    return payload

def channels_create_http(token, name, is_public):
    '''channels create http'''
    #POST Request
    data = json.dumps({
        "token" : token,
        "name" : name,
        "is_public" : is_public
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    print("Created channel with channel_id: " + str(payload["channel_id"]))
    return payload

def channel_invite_http(token, channel_id, u_id):
    '''channel invite http'''
    #POST Request
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "u_id" : u_id
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/channel/invite",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    return payload

def channel_messages_http(token, channel_id, start):
    '''channel messages http'''
    #GET
    print(f"Channel_message_http:\n")
    query_string = urllib.parse.urlencode({
        "token" : token,
        "channel_id" : channel_id,
        "start" : start
    })
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messages?{query_string}")
    payload = json.load(response)
    return payload


def standup_start_http(token, channel_id, length):
    '''standup start http'''
    #POST Request
    print(f"standup_start_http: {type(channel_id)}\n")
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "length" : length
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/standup/start",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    return payload

def standup_active_http(token, channel_id):
    '''standup active http'''
    #GET
    print(f"standup_active_http: {type(channel_id)}\n")
    query_string = urllib.parse.urlencode({
        "token" : token,
        "channel_id" : int(channel_id)
    })
    response = urllib.request.urlopen(f"{BASE_URL}/standup/active?{query_string}")
    payload = json.load(response)
    return payload

def standup_send_http(token, channel_id, message):
    '''standup send http'''
    #POST
    data = json.dumps({
        "token" : token,
        "channel_id" : channel_id,
        "message" : message
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/standup/send",
        data=data,
        headers={"Content-Type": "application/json"}
    )

    payload = json.load(urllib.request.urlopen(req))
    return payload

if __name__ == "__main__":
    try:
        BASE_URL = "http://127.0.0.1:" + str(sys.argv[1])
    except: # pylint: disable=bare-except
        PORT = input("What is the port number?")
        BASE_URL = "http://127.0.0.1:" + str(PORT)
    #Run these tests
    auth_register_http(user1)
    auth_register_http(user2)
    # time.sleep(1)
    # auth_login_http(user1)
    # time.sleep(1)
    # auth_login_http(user1)
    # time.sleep(1)
    # auth_login_http(user1)
    # channel_id = channels_create_http(user1["token"], "MyChannel", True)["channel_id"]
    # print(type(channel_id))
    # print(standup_active_http(user1["token"], channel_id))
    # standup_start_http(user1["token"], channel_id, 5)
    # message_id = message_send_http(user1["token"], channel_id, "hello im samuel")["message_id"]
    # message_react(user1["token"], message_id, 1)
    # message_unreact(user1["token"], message_id, 1)
    # standup_send_http(user1["token"], channel_id, "Hello i'm david")
    # standup_send_http(user1["token"], channel_id, "Thats pretty cool")
    # print(channel_messages_http(user1["token"], channel_id, 0))
    # channel_invite_http(user1["token"], channel_id, user2["u_id"])
    # time.sleep(1)
    # print(standup_active_http(user1["token"], channel_id))
    # time.sleep(5)
    # print(standup_active_http(user1["token"], channel_id))
    # print(channel_messages_http(user1["token"], channel_id, 0))
    
"""This module is designed for the system_test"""
import json
import urllib.request
import urllib.parse
from projectDefines import user1
from urllibHelper import auth_register_http, auth_login_http, channels_create_http
from urllibHelper import standup_start_http, standup_active_http, standup_send_http

BASE_URL = "http://127.0.0.1:5052"

def test_workspace_reset():
    '''resets workplace'''
    #Reset everthing make sure the work space is clean
    req = urllib.request.Request(f"{BASE_URL}/workspace/reset", method='POST')
    with urllib.request.urlopen(req) as response:
        json_response = json.load(response)
    assert json_response == {}

def test_standup_start():
    '''Tests standup start'''
    test_workspace_reset()
    auth_register_http(user1)
    auth_login_http(user1)
    channel_id = channels_create_http(user1["token"], "MyChannel", True)["channel_id"]
    standup_start_http(user1["token"], channel_id, 5)

def test_standup_active():
    '''Tests standup active'''
    test_workspace_reset()
    auth_register_http(user1)
    auth_login_http(user1)
    channel_id = channels_create_http(user1["token"], "MyChannel", True)["channel_id"]
    standup_start_http(user1["token"], channel_id, 5)
    assert standup_active_http(user1["token"], channel_id)["is_active"]

def test_standup_send():
    '''Tests startup send'''
    test_workspace_reset()
    auth_register_http(user1)
    auth_login_http(user1)
    channel_id = channels_create_http(user1["token"], "MyChannel", True)["channel_id"]
    standup_start_http(user1["token"], channel_id, 5)
    assert standup_send_http(user1["token"], channel_id, "Hello") == {}

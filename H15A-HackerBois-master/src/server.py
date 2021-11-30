'''This module implements server'''
import sys
from json import dumps
from flask import Flask, request, send_file
from flask_cors import CORS
from auth import auth_login, auth_register, auth_logout, auth_password_reset_request, auth_password_reset_reset # pylint: disable=line-too-long
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join
from channel import channel_addowner, channel_removeowner
from channels import channels_list, channels_listall, channels_create
from message import message_send, message_remove, message_edit, message_react, message_unreact, message_pin, message_unpin, message_sendlater # pylint: disable=line-too-long
from standup import standup_start, standup_active, standup_send
from user import user_profile, user_profile_setname, user_profile_setemail, user_profile_sethandle, user_profile_uploadphoto
from other import users_all, search
from admin import admin_userpermission_change, admin_user_remove
from error import InputError
from database import database

def get_database():
    '''returns database'''
    return database

def default_handler(err):
    '''handler'''
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, default_handler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    '''echo'''
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

#Test Main page
@APP.route("/")
def hello_world():
    '''checks if server is on'''
    return "Hello, if you see me, you have connected to the browser! Very nice!"

@APP.route("/workspace/save", methods=['POST'])
def save():
    '''save state of server'''
    database.save()
    return dumps({})

@APP.route("/workspace/get", methods=['POST'])
def get():
    '''Displays state of server'''
    output = database.get_data()
    return dumps(output)

#Auth.py
@APP.route("/auth/login", methods=['POST'])
def login():
    '''login'''
    data = request.get_json()
    output = auth_login(data["email"], data["password"])
    #print("Active Users: " + str(database.getActiveUserList()) + "\n")
    return dumps({
        'u_id': output['u_id'],
        'token': output['token']
    })

@APP.route("/auth/register", methods=['POST'])
def register():
    '''register'''
    data = request.get_json()
    output = auth_register(data["email"], data["password"], data["name_first"], data["name_last"])
    #print("users: "+ str(database.getAllUsers()) + "\n")
    return dumps({
        'u_id': output['u_id'],
        'token': output['token']
    })

@APP.route("/auth/logout", methods=['POST'])
def logout():
    '''logout'''
    data = request.get_json()
    output = auth_logout(data["token"])
    return dumps(output)

@APP.route("/auth/passwordreset/request", methods=['POST'])
def reset_request():
    '''reset_request'''
    data = request.get_json()
    output = auth_password_reset_request(data["email"])
    return dumps(output)

@APP.route("/auth/passwordreset/reset", methods=['POST'])
def reset_reset():
    '''reset_reset'''
    data = request.get_json()
    output = auth_password_reset_reset(data["reset_code"], data["new_password"])
    return dumps(output)

#channel.py
@APP.route("/channel/invite", methods=['POST'])
def invite():
    '''invite'''
    data = request.get_json()
    output = channel_invite(data["token"], int(data["channel_id"]), int(data["u_id"]))
    return dumps(output)

@APP.route("/channel/details", methods=['GET'])
def details():
    '''details'''
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    output = channel_details(token, channel_id)
    return dumps(output)

@APP.route("/channel/messages", methods=['GET'])
def messages():
    '''messages'''
    token = str(request.args.get('token'))
    channel_id = int(request.args.get('channel_id'))
    start1 = int(request.args.get('start'))
    output = channel_messages(token, channel_id, start1)
    return dumps(output)

@APP.route("/channel/leave", methods=['POST'])
def leave():
    '''leave'''
    data = request.get_json()
    output = channel_leave(data["token"], int(data["channel_id"]))
    return dumps(output)

@APP.route("/channel/join", methods=['POST'])
def join():
    '''join'''
    data = request.get_json()
    output = channel_join(data["token"], int(data["channel_id"]))
    return dumps(output)

@APP.route("/channel/addowner", methods=['POST'])
def addowner():
    '''addowner'''
    data = request.get_json()
    output = channel_addowner(data["token"], int(data["channel_id"]), int(data['u_id']))
    return dumps(output)

@APP.route("/channel/removeowner", methods=['POST'])
def removeowner():
    '''removeowner'''
    data = request.get_json()
    output = channel_removeowner(data["token"], int(data["channel_id"]), int(data['u_id']))
    return dumps(output)

#channels.py
@APP.route("/channels/list", methods=['GET'])
def _list():
    '''list'''
    token = str(request.args.get('token'))
    output = channels_list(token)
    return dumps(output)

@APP.route("/channels/listall", methods=['GET'])
def _listall():
    '''listall'''
    token = str(request.args.get('token'))
    output = channels_listall(token)
    return dumps(output)

@APP.route("/channels/create", methods=['POST'])
def create():
    '''create'''
    data = request.get_json()
    output = channels_create(data['token'], data['name'], data['is_public'])
    return dumps(output)

@APP.route("/message/send", methods=['POST'])
def send():
    '''send'''
    data = request.get_json()
    output = message_send(data['token'], int(data['channel_id']), data['message'])
    return dumps(output)

@APP.route("/message/sendlater", methods=['POST'])
def sendlater():
    '''sendlater'''
    data = request.get_json()
    output = message_sendlater(data['token'], int(data['channel_id']), data['message'], data['time_sent']) # pylint: disable=line-too-long
    return dumps(output)

@APP.route("/message/react", methods=['POST'])
def react():
    '''react'''
    data = request.get_json()
    output = message_react(data['token'], int(data['message_id']), int(data['react_id']))
    return dumps(output)

@APP.route("/message/unreact", methods=['POST'])
def unreact():
    '''unreact'''
    data = request.get_json()
    output = message_unreact(data['token'], int(data['message_id']), int(data['react_id']))
    return dumps(output)

@APP.route("/message/pin", methods=['POST'])
def pin():
    '''pin'''
    data = request.get_json()
    output = message_pin(data['token'], int(data['message_id']))
    return dumps(output)

@APP.route("/message/unpin", methods=['POST'])
def unpin():
    '''unpin'''
    data = request.get_json()
    output = message_unpin(data['token'], int(data['message_id']))
    return dumps(output)

@APP.route("/message/remove", methods=['DELETE'])
def remove():
    '''remove'''
    data = request.get_json()
    output = message_remove(data['token'], int(data['message_id']))
    return dumps(output)

@APP.route("/message/edit", methods=['PUT'])
def edit():
    '''edit'''
    data = request.get_json()
    output = message_edit(data['token'], int(data['message_id']), data['message'])
    return dumps(output)

# User
@APP.route("/user/profile", methods=['GET'])
def profile():
    '''profile'''
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    output = user_profile(token, u_id)
    return dumps(output)

@APP.route("/user/profile/setname", methods=['PUT'])
def edit_name():
    '''edit name'''
    data = request.get_json()
    output = user_profile_setname(data['token'], data['name_first'], data['name_last'])
    return dumps(output)

@APP.route("/user/profile/setemail", methods=['PUT'])
def edit_email():
    '''edit email'''
    data = request.get_json()
    output = user_profile_setemail(data['token'], data['email'])
    return dumps(output)

@APP.route("/user/profile/sethandle", methods=['PUT'])
def edit_handle():
    '''edit handle'''
    data = request.get_json()
    output = user_profile_sethandle(data['token'], data['handle_str'])
    return dumps(output)

#Set profile photo
@APP.route("/user/profile/uploadphoto", methods=['POST'])
def upload_photo():
    '''upload profile photo'''
    data = request.get_json()
    try:
        output = user_profile_uploadphoto(data['token'], data['img_url'], int(data['x_start']), int(data['y_start']), int(data['x_end']), int(data['y_end']))
        return dumps(output)
    except KeyError:
        raise InputError(description="Invalid input!")

@APP.route("/imgurl/<image_link>")
def imgurl(image_link):
    '''Adds the image to the folder'''
    try:
        return send_file(f'user_images/{image_link}', mimetype='image/jpg')
    except:
        return dumps({})

# Other
@APP.route("/users/all", methods=['GET'])
def all_u():
    '''all user'''
    token = request.args.get('token')
    output = users_all(token)
    return dumps(output)

@APP.route("/search", methods=['GET'])
def other_search():
    '''other search'''
    token = request.args.get('token')
    query = request.args.get('query_str')
    output = search(token, query)
    return dumps(output)

# Admin
@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermission():
    '''admin userpermission'''
    data = request.get_json()
    admin_userpermission_change(data['token'], int(data['u_id']), int(data['permission_id']))
    return dumps({})

@APP.route("/admin/user/remove", methods=['DELETE'])
def admin_remove_user():
    '''admin remove user'''
    data = request.get_json()
    admin_user_remove(data['token'], int(data['u_id']))
    return dumps({})

# Standup
@APP.route("/standup/start", methods=['POST'])
def start():
    '''start'''
    data = request.get_json()
    output = standup_start(data['token'], int(data['channel_id']), int(data['length']))
    return dumps(output)

@APP.route("/standup/active", methods=['GET'])
def active():
    '''active'''
    token = request.args.get('token')
    #Convert channel_id from string back to int
    channel_id = int(request.args.get('channel_id'))
    #print(f"standup_active ROUTE: {type(channel_id)}\n")
    output = standup_active(token, channel_id)
    return dumps(output)

@APP.route("/standup/send", methods=['POST'])
def standup_message():
    '''message'''
    data = request.get_json()
    output = standup_send(data["token"], int(data["channel_id"]), data["message"])
    return dumps(output)

@APP.route("/workspace/reset", methods=['POST'])
def reset():
    '''reset'''
    database.reset()
    database.remove_images()
    database.remove_save_file()
    return dumps({})

if __name__ == "__main__":
    APP.run(port=(int(sys.argv[1]) if len(sys.argv) == 2 else 5052), debug=True)

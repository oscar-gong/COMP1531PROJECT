'''This file contains the structure of the database for the project
and contains the structure of other classes'''
import hashlib
import os
import random
from datetime import datetime, timezone
import threading
import time
import pickle
import shutil
import math
from error import InputError

class ServerDatabase():
    '''
    ServerDatabase acts as the "server" class which contains all the users, 
    channels, messages and so on. Everything in the server is stored 
    in an instance of this class
    '''
    def __init__(self):
        self.reset()
        #Set up autosaving thread
        self.start_auto_save()

    #This is called to set all the intial values of the database
    #This is also called to reset the database
    def reset(self):
        '''Resets the whole server, deleting also the savefile'''
        self.remove_save_file()
        #This stores all the registered users as UserEntity objects
        self.registered_users = []

        #Stores a dictionary of all the users currently requesting
        #a password reset
        self.users_reset = {}

        self.auto_save_time = 10
        #This stores all the currently logged in users as a dictionary
        #They key is the token whilst the value is the UserEntity
        self.active_users = {}

        #This stores all the channels in the same way as active_users
        #channel_id is the key whilst the ChannelObject is the value
        self.channels = {"channels":[]}

        #Reset everytime but then increment until the unviverse explodes
        self.channel_id = 0
        #Reset everytime but then increment until the unviverse explodes
        self.user_id = 0

        #Reset everytime but then increment until the unviverse explodes
        self.message_id = 0

    def remove_images(self):
        '''Removes images from folder'''
        folder = 'user_images'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if filename != "bot.jpg" and filename != ".gitignore":
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

    def remove_save_file(self):
        '''Deletes save file'''
        if os.path.exists("server_save.p"):
            os.remove("server_save.p")
            print("Save file deleted successfully\n")

    #Saves the current state of the server
    def save(self):
        '''Saves the current server state'''
        with open('server_save.p', 'wb') as save_file:
            pickle.dump(self, save_file)

    def auto_save(self):
        '''Periodically automatically saves the state of the server.
        The time between each save is set in the ServerDatabase class
        as an attribute called auto_save_time
        '''
        while True:
            self.save()
            print(f"Saved server state at {datetime.utcnow()}\n")
            time.sleep(self.auto_save_time)

    def start_auto_save(self):
        '''starts a separate thread for autosave'''
        threading.Thread(target=self.auto_save, daemon=True).start()

    def get_data(self):
        '''Gets and returns all the data of the server. 
        Useful for testing to see what is currently in the server'''
        return {
            "registered_users" : self.get_all_users(),
            "active_users" : self.get_all_active_users(),
            "channels" : self.get_all_channels(),
            "channel_id" : self.channel_id,
            "user_id" : self.user_id,
            "message_id" : self.message_id
        }

    def remove_user(self, user):
        '''Finds and removes the given user Object from database'''
        token = user.get_token()
        if token in self.active_users:
            del self.active_users[token]
        self.registered_users.remove(user)

    #Returns a dictionary containing the token as the key
    #and the user email as the value
    def get_message_by_id(self, message_id):
        '''Returns a message dictionary given its id'''
        for channel in self.channels["channels"]:
            message = channel.get_message_by_id(message_id)
            if message is not None:
                return {
                    "message" : message,
                    "channel" : channel
                }
        raise InputError(description="Invalid message id")

    def get_message_object_by_id(self, message_id):
        '''Returns a message object given its id'''
        for channel in self.channels["channels"]:
            if channel.contains_message(message_id):
                return channel.get_message_by_id(message_id)
        raise InputError(description="Invalid message id")

    def get_channel_by_message_id(self, message_id):
        '''used to get channel object by message id'''
        for channel in self.channels["channels"]:
            if channel.contains_message(message_id):
                return channel

    def user_channel_list(self, u_id):
        '''used to get a list of channels a member is a part of'''
        output = []
        for channel in self.channels['channels']:
            if channel.member_in_channel(u_id):
                output.append(channel)
        return output

    def get_active_user_by_u_id(self, u_id):
        '''used to get active user by user id'''
        for value in self.active_users.values():
            if value.u_id == u_id:
                return value
        return None

    #Returns the UserEntity object when given a user's token
    def get_user_object(self, token):
        '''used to get user object by token'''
        try:
            return self.active_users[token]
        except KeyError as error:
            print("This is the error: " + str(error))
            return "NOT_FOUND"

    def get_user_by_reset_code(self, code):
        '''get registered user by reset code'''
        for user in self.registered_users:
            if user.reset_code == code:
                return user
        return None

    def get_user_object_by_id(self, u_id):
        '''used to get user object by user id'''
        for user in self.registered_users:
            if user.u_id == u_id:
                return user
        return "NOT_FOUND"

    def get_user_object_by_email(self, email):
        '''used to get user object by email'''
        for user in self.registered_users:
            if user.email == email:
                return user
        return None

    def is_in_channel(self, channel_id):
        '''Checks if the channel_id is in the server's list of channels'''
        for channel in self.channels["channels"]:
            if channel_id == channel.channel_dict()['channel_id']:
                return True
        return False

    def get_channel_by_id(self, channel_id):
        '''used to get channel by id'''
        for channel in self.channels['channels']:
            if channel_id == channel.channel_id:
                return channel
        return None

    def get_all_users(self):
        '''Returns all the registered users as a list of dictionaries'''
        output = []
        for user_object in self.registered_users:
            output.append(user_object.get_user())
        return output

    def get_all_active_users(self):
        '''Returns all the active users as a list of dictionaries'''
        output = []
        for user_object in self.active_users.values():
            output.append(user_object.get_user())
        return output

    def get_all_channels(self):
        '''Returns all the active channels as a list of channel names'''
        output = []
        for channel in self.channels["channels"]:
            output.append(channel.name)
        return output

    def get_all_handles(self):
        '''Returns all the registered user handles as a list'''
        output = []
        for user_object in self.registered_users:
            output.append(user_object.handle_str)
        return output

    def get_last_channel_id(self):
        '''used to get last channel id'''
        return self.channel_id

    def update_last_channel_id(self):
        '''used to update last channel id'''
        self.channel_id = self.channel_id + 1 # pylint: disable=attribute-defined-outside-init

    def add_channel_to_list(self, new_channel):
        '''used to add channel to the list of channels'''
        self.channels['channels'].append(new_channel)

    def update_last_message_id(self):
        '''updates last message id'''
        self.message_id = self.message_id + 1 # pylint: disable=attribute-defined-outside-init

    def get_last_message_id(self):
        '''gets last message id'''
        return self.message_id

    def get_owner_list(self):
        '''gets owner list'''
        output = []
        for users in self.registered_users:
            if users.permission_id == 1:
                output.append(users)
        return output


class UserEntity(): # pylint: disable=too-many-instance-attributes
    '''All users are created as UserEntity objects. It contains the users email,
    password, first and last name,u_id, handle string, current token, permission id, reset code
    if one is currently active and the users profile'''
    def __init__(self, email, password, name_first, name_last, u_id, handle_str, permission_id): # pylint: disable=too-many-arguments
        self.email = email
        self.password = password
        self.name_first = name_first
        self.name_last = name_last
        self.u_id = u_id
        self.handle_str = handle_str
        self.token = ''
        self.permission_id = permission_id
        self.reset_code = None
        self.profile_img_url = ''

    def generate_reset_code(self):
        '''Generates a reset code, set it for userobject and return it'''
        reset_code = self.generate_token()
        self.reset_code = reset_code
        return reset_code

    def generate_token(self):
        '''Generates a token using a users password and u_id ensuring no duplicate tokens can be
        created since no one can have the same u_id. Also add a random integer at the end to make
        sure the token is different every time'''
        i = self.password + str(self.u_id) + str(random.random())
        return hashlib.sha256(i.encode()).hexdigest()

    def get_user(self):
        '''Returns a user dictionary (as defined by the spec)'''
        return {
            "u_id": self.u_id,
            "email": self.email,
            "name_first": self.name_first,
            "name_last": self.name_last,
            "handle_str": self.handle_str,
            "profile_img_url":self.profile_img_url
        }

    def edit_user_name(self, firstname, lastname):
        '''edits username'''
        self.name_first = firstname
        self.name_last = lastname

    def edit_user_email(self, email):
        '''edits email'''
        self.email = email

    def edit_user_handle(self, handle):
        '''edits user handle'''
        self.handle_str = handle

    def get_img_url(self):
        '''gets user img url'''
        return self.profile_img_url

    def get_token(self):
        '''gets user token'''
        return self.token

    def get_permission_id(self):
        '''gets permission id'''
        return self.permission_id

    def set_token(self, token):
        '''sets token'''
        self.token = token

    def set_permission_id(self, p_id):
        '''sets permission id'''
        self.permission_id = p_id

    def set_profile_image_url(self, url):
        '''sets profile image url'''
        self.profile_img_url = url

class ChannelObject(): # pylint: disable=too-many-instance-attributes
    '''Structure of a Channel'''
    def __init__(self, owner, name, is_public, channel_id):
        self.owner = owner
        self.name = name
        self.is_public = is_public
        self.channel_id = channel_id
        self.owner_members = []
        self.all_members = []
        #This should be a list of message_objects
        self.messages = []
        self.pinned_count = 0
        self.standup_queue = []
        self.standup_info = {
            "active" : False,
            "time_finish" : None,
            "start_user" : None
        }
        self.hangman_info = {
            "state_count": -1,
            "word": "",
            "guessed_letters": [],
            "word_guess": []
        }

    def channel_dict(self):
        '''gets a dictionary of channel'''
        channel = {
            'token': self.owner,
            'name': self.name,
            'is_public':self.is_public,
            'channel_id':self.channel_id,
            'owner_members':self.owner_members,
            'all_members': self.all_members,
            'messages':self.messages
        }
        return channel

    def channel_details(self):
        '''gets channel details dictionary'''
        channel = {
            'channel_id':self.channel_id,
            'name': self.name
        }
        return channel

    def start_hangman(self, new_word):
        '''Initialises hangman game'''
        self.hangman_info = {
            "state_count": 0,
            "word": new_word,
            "guessed_letters": [],
            "word_guess": []
        }
        for letter in new_word:
            if letter == "'":
                self.hangman_info['word_guess'].append("'")
            else:
                self.hangman_info['word_guess'].append("_")
        return self.hangman_info

    def get_hangman_state(self):
        '''returns the hangman info'''
        return self.hangman_info

    def fill_hangman_letter(self, letter, position):
        '''fill in the correctly guessed letter in word_guess list'''
        self.hangman_info["word_guess"][position] = letter

    def add_hangman_letter(self, letter):
        '''add the incorrectly guess letter in guessed_letters list'''
        self.hangman_info["guessed_letters"].append(letter)

    def increment_hangman_state_count(self):
        '''increment hangman state count'''
        self.hangman_info["state_count"] += 1

    def hangman_end(self):
        '''set hangman state count to -1'''
        self.hangman_info["state_count"] = -1

    def increment_pinned_count(self):
        '''increment pinned count'''
        self.pinned_count += 1

    def decrement_pinned_count(self):
        '''decrement pinned count'''
        self.pinned_count -= 1

    def insert_message_by_id(self, message):
        '''insert message by id'''
        for i in range(len(self.messages)):
            if self.messages[i].message_id < message.message_id:
                self.messages.insert(i, message)
                return
        self.messages.append(message)

    def add_owner(self, user):
        '''adds owner'''
        self.owner_members.append(user)

    def remove_owner(self, user):
        '''removes owner'''
        self.owner_members.remove(user)

    def add_member(self, user):
        '''adds member'''
        self.all_members.append(user)

    def remove_member(self, user):
        '''removes member'''
        self.all_members.remove(user)
        if self.is_owner(user):
            self.owner_members.remove(user)

    def is_owner(self, user):
        '''checks if owner'''
        return user in self.owner_members

    def get_number_of_messages(self):
        '''returns number of messages'''
        return len(self.messages)

    def member_in_channel(self, u_id):
        '''checks if member is in channel'''
        for member in self.all_members:
            if u_id == member.u_id:
                return True
        return False

    def get_owner_detail_list(self):
        '''gets a list of owner details'''
        owner_list = []
        for owner in self.owner_members:
            owner_details = {
                "u_id" : owner.u_id,
                "name_first" : owner.name_first,
                "name_last" : owner.name_last,
                "profile_img_url":owner.profile_img_url
            }
            owner_list.append(owner_details)
        return owner_list

    def get_user_detail_list(self):
        '''gets of list of user details'''
        user_list = []
        for user in self.all_members:
            user_details = {
                "u_id" : user.u_id,
                "name_first" : user.name_first,
                "name_last" : user.name_last,
                "profile_img_url":user.profile_img_url
            }
            user_list.append(user_details)
        return user_list

    def add_message_to_channel(self, message_obj):
        '''adds a message to channel'''
        self.messages.insert(self.pinned_count, message_obj)

    def contains_message(self, message_id):
        '''checks if channel contains message'''
        for message in self.messages:
            if message.message_id == message_id:
                return True
        return False

    def get_message_by_id(self, message_id):
        '''gets message by id'''
        for message in self.messages:
            if message.message_id == message_id:
                return message
        return None

    def remove_user_messages_by_u_id(self, user_id):
        '''remove user messages by user id'''
        for message in reversed(self.messages):
            if message.get_u_id() == user_id:
                self.messages.remove(message)

    def remove_user_reacts_by_u_id(self, user_id):
        '''remove user reacts by user id'''
        for message in self.messages:
            reacts = message.get_reacts()
            for react in reacts:
                react.remove_user_from_reacts(user_id)

    def standup_end(self):
        '''end startup'''
        #Get the user who started the standup
        user = self.standup_info["start_user"]
        #Create a message id for the standup message
        msg_id = database.get_last_message_id()
        #Loop through and fill the message output
        msg_str = ""

        #Generate the packaged message
        curr_speaker_u_id = None
        for message in self.standup_queue:
            #Add the user of a new message
            if message.u_id != curr_speaker_u_id:
                if curr_speaker_u_id is not None:
                    msg_str = msg_str + "\n"
                curr_speaker_u_id = message.u_id
            if database.get_user_object_by_id(curr_speaker_u_id).name_first != "NOT_FOUND":
                msg_str = msg_str + database.get_user_object_by_id(curr_speaker_u_id).name_first + ": " # pylint: disable=line-too-long
                #Add the message
                msg_str = msg_str + message.get_standup_message() + "\n"
        output_message = MessageObject(user.u_id, msg_str, msg_id)
        self.add_message_to_channel(output_message)
        database.update_last_message_id()
        self.standup_queue = []


    def start_standup_timer(self, length):
        '''start standup timer'''
        threading.Thread(target=self.standup_timer, args=(length,)).start()
        #threading.Thread(target=self.standupDebug, args=(length,)).start()

    # def standupDebug(self, length):
    #     for i in range(length + 2):
    #         print("StandupActive: " + str(self.standup_info["active"])
    # + " standup_end: " + str(self.standup_info["time_finish"]))
    #         time.sleep(1)
    #Do not call this function to start the standup timer
    #Call the startstandup_timer as it makes a separate thread

    def standup_timer(self, length):
        '''standup timer'''
        #print("Start standup_timer at: " + str(datetime.utcnow().replace
        # (tzinfo=timezone.utc).timestamp()) + "\n")
        #Set standup for channel to active
        self.standup_info["active"] = True
        #Wait for the length
        time.sleep(length)
        #Post the packaged message
        self.standup_end()
        #Set standup for channel back to inactive
        self.standup_info["active"] = False
        self.standup_info["time_finish"] = None
        self.standup_info["start_user"] = None
        #print("Ending standup_timer at: " + str(datetime.utcnow().
        # replace(tzinfo=timezone.utc).timestamp()) + "\n")

    def send_message_now(self, msg):
        '''sends the message now'''
        msg.time_created = math.floor(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        #Add the message object to channel
        self.add_message_to_channel(msg)

class MessageObject():
    '''Structure of a message'''
    def __init__(self, u_id, message, message_id):
        self.message_id = message_id
        self.u_id = u_id
        self.message = message
        self.time_created = math.floor(datetime.utcnow().replace(tzinfo=timezone.utc).timestamp())
        self.reacts = []
        self.is_pinned = False
    #Returns a dictionary containing message info as required by spec
    def get_message(self, u_id):
        '''gets message'''
        return {
            "message_id": self.message_id,
            "u_id":self.u_id,
            "message": self.message,
            "time_created": self.time_created,
            "reacts": self.get_reacts_list(u_id),
            "is_pinned": self.is_pinned
        }

    def get_reacts_list(self, u_id):
        '''Returns the list of reacts'''
        output = []
        for react in self.reacts:
            output.append(react.get_reacts(u_id))
        return output

    def set_pinned(self):
        '''sets pin'''
        self.is_pinned = True

    def set_un_pinned(self):
        '''removes pin'''
        self.is_pinned = False

    def edit_message(self, message):
        '''edits message'''
        self.message = message

    def get_standup_message(self):
        '''gets standup message'''
        return self.message

    def add_reacts_object(self, reacts):
        '''adds a react object'''
        self.reacts.append(reacts)

    def get_u_id(self):
        '''gets_u_id'''
        return self.u_id

    def get_reacts(self):
        '''gets list of react object'''
        return self.reacts

#List of dictionaries, where each dictionary contains types { react_id, u_ids, is_this_user_reacted}
#where react_id is the id of a react, and u_ids is a list of user id's of people who've reacted for
# that react. is_this_user_reacted is whether or not the authorised user has been one of
# the reacts to this post

class ReactObject():
    '''Structure of a react'''
    def __init__(self, react_id, u_ids):
        self.react_id = react_id
        self.u_ids = [u_ids]

    #Checks if for a given u_id if the user has reacted it
    def is_this_user_reacted(self, input_u_id):
        '''Checks to see if the user has reacted'''
        if input_u_id in self.u_ids:
            return True
        return False

    def get_reacts(self, u_id):
        '''gets reacts'''
        return {
            "react_id": self.react_id,
            "u_ids": self.u_ids,
            "is_this_user_reacted": self.is_this_user_reacted(u_id)
        }
    def add_u_id_in(self, u_id):
        '''add user id in'''
        self.u_ids.append(u_id)
    def remove_user_from_reacts(self, u_id):
        '''removes react'''
        if u_id in self.u_ids:
            self.u_ids.remove(u_id)

def load_database():
    '''Create an instance of the ServerDatabase class
    Any changes done to the database will be done to this instance'''
    data = None
    try:
        #Get absolute path of server_save.p
        my_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(my_path, "server_save.p")
        data = pickle.load(open(path, "rb"))
        data.start_auto_save()
        print(f"Data save found at location: {path}\n")
        print(f"Starting Server State:\n {str(data.get_data())}\n")
    except IOError:
        print("DATA SAVE NOT FOUND\n")
        data = ServerDatabase()
    except EOFError:
        data = ServerDatabase()
    return data

database = load_database()

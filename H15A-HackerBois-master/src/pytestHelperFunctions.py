'''This file contains a bunch of helper functions that may help during tests'''
from auth import auth_login, auth_register


#This function takes in a user dictionary, with the same keys as the ones defined in projectDefines
#and registers the user. Returns the user with the u_id and token updated.
# Returns the token USER_EXISTS
#if the user already exists and cannot be registered
def create_user(user):
    '''Creates user '''
    #Assumes that auth_register works
    output = auth_register(user["email"], user["password"], user["name_first"], user["name_last"])
    user["u_id"] = output["u_id"]
    user["token"] = output["token"]
    return user


#Creates a logged in User and returns the user with its u_id and token updated.
#If the user does not exist, it is created
def create_login_user(input_user):
    '''Creates login user'''
    #Tries to create the user
    user_data = create_user(input_user)

    #Logs in to the given user
    #try:
    output = auth_login(user_data["email"], user_data["password"])
    input_user["u_id"] = output["u_id"]
    input_user["token"] = output["token"]
    #except:
        #input_user["token"] = "CANNOT_LOGIN"

    return input_user


#When given a user dictionary, returns a new dictionary with just the keys required for
#the members variable name given in the spec

def change_to_member(user):
    '''Change to member'''
    return {
        "u_id" : user["u_id"],
        "name_first" : user["name_first"],
        "name_last" : user["name_last"],
        "profile_img_url" : user["profile_img_url"]
        }

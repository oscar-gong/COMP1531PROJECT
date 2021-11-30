"""
This module implements all the authentication functions of the project
"""
import smtplib
import ssl
from projectHelperFunctions import is_valid_email
from error import InputError
from database import database, UserEntity


#Takes in an email and password and returns u_id and token if valid
def auth_login(email, password):
    '''
    Takes in an email string and a password string and returns a newly login generated token.
    Checks the email and password making sure it is valid
    '''
    #Error Checking
    if not is_valid_email(email):
        raise InputError(description='Not a valid email')
    elif not email_already_registered(email):
        raise InputError(description='Your email has not been registered')

    #Fetch the user from database
    new_user = get_user(email, password)

    #Checks if the correct password is given
    if new_user == "ERROR":
        raise InputError(description='Incorrect username or password')

    #Check if the user is already logged in
    if database.get_active_user_by_u_id(new_user.u_id) is not None:
        #Logs the user out
        del database.active_users[new_user.token]


    #Generates a new active token and logs the user in
    new_user.set_token(new_user.generate_token())
    database.active_users[new_user.token] = new_user

    return {
        "u_id": new_user.u_id,
        "token": new_user.token
    }


def auth_logout(token):
    '''
    Given an active token, logs the user out
    '''
    #Checking to see if the token is valid
    if token in database.active_users:
        #Log out the user by deleting the key value pair from the dictionary
        del database.active_users[token]
        return {
            "is_success": True
        }

    #User is not logged in
    return {
        "is_success": False
        }



def auth_register(email, password, name_first, name_last):
    '''
    Given a valid email, password and first and last name,
    create a new user and return its u_id and token. This
    also automatically logs the user in
    '''
    #Error checking
    if not is_valid_email(email):
        raise InputError(description='Not a valid email')
    elif email_already_registered(email):
        raise InputError(description='Email already registered')
    elif len(password) < 6:
        raise InputError(description='Length of password is too short')
    elif not (len(name_first) >= 1 and len(name_first) <= 50):
        raise InputError(description='First name is not correct length')
    elif not (len(name_last) >= 1 and len(name_last) <= 50):
        raise InputError(description='Last name is not correct length')

    #Create a new handle for the user
    user_handle = create_handle(name_first, name_last)

    #The u_id generated is simply the position of the user registered
    #For example, the first user registered has u_id 0, 2nd has u_id 1 and so on
    new_u_id = len(database.registered_users)

    perimission_id = 2
    if new_u_id == 0:
        perimission_id = 1

    #Creating a new instance of the user using the previously made values
    new_user = UserEntity(email, password, name_first, name_last, new_u_id, user_handle, perimission_id)

    #Generate new active token for the user
    new_user.set_token(new_user.generate_token())

    #Store the user into the registered_users database
    database.registered_users.append(new_user)

    #Logs in the user
    database.active_users[new_user.token] = new_user

    #Return u_id and token
    return {
        "u_id": new_user.u_id,
        "token": new_user.token
    }


def auth_password_reset_request(email):
    '''
    When given an email string, search the database for the user.
    If the user exists, send an email to the user containing a freshly
    generated reset code.
    '''
    user = database.get_user_object_by_email(email)
    if user is not None:
        email_message = f"Hello {user.name_first},\n"
        email_message = email_message + f"Your reset code is {str(user.generate_reset_code())}"
        print(email_message)
        send_email(email, email_message)
    else:
        print("User can't be found\n")
    return {}

def auth_password_reset_reset(reset_code, new_password):
    '''
    Given a valid reset code and valid new password,
    reset the users password
    '''
    if len(new_password) < 6:
        raise InputError(description="Invalid password")
    user = database.get_user_by_reset_code(reset_code)
    if user is not None:
        user.password = new_password
        #Disable reset code
        user.reset_code = None
    else:
        raise InputError(description="Invalid reset code")
    return {}

#Checks if an email is already registered
def email_already_registered(email):
    '''Given an email, check if it has been registered'''
    for user in database.registered_users:
        if user.email == email:
            return True
    return False


#Searches the registered_users database for a user when given
#an email and password and see if it matches the one given in the
#database
#Returns the user object on success
#Else return an "ERROR" string
def get_user(email, password):
    '''Given a valid email and password, return the user object'''
    #Assumes the user exists
    for user in database.registered_users:
        #Checks if the correct email and username is given
        if user.email == email:
            if user.password == password:
                return user
    return "ERROR"


#Creates a new handle that does not exist yet
def create_handle(name_first, name_last):
    '''Generates a new handle using the first and last name of a user'''
    #Get a list of all existing handles
    existing_handles = database.get_all_handles()
    concatenation = name_first.lower() + name_last.lower()
    user_handle = concatenation
    i = 0

    #Checks if the generated user_handle exists
    #If it does add a number to the user_handle
    #Keeps doing so until the user_handle does not exist
    while user_handle in existing_handles:
        user_handle = concatenation + str(i)
        i += 1

    return user_handle

def send_email(target_email, message):
    """
    Given an email address and a message string, sending it as a plain
    text email to the target email
    """
    bot_email = "slackr2412@gmail.com"
    password = "PythonIsCool24"

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(bot_email, password)
        server.sendmail(bot_email, target_email, message)

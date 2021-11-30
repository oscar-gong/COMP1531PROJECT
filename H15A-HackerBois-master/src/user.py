'''This module implements user handling functions'''
import random
import string
import urllib
from PIL import Image
from database import database
from projectHelperFunctions import is_valid_email
from error import InputError, AccessError
SERVER_PORT = 5052
#Checks if an email is already registered
def email_already_used(email):
    '''Checks if the given email has already been
    registered or not'''
    for user in database.registered_users:
        if user.email == email:
            return True
    return False

#Checks if a handle has already been used
def handle_already_used(handle):
    '''check if a handle already has been used'''
    for user in database.registered_users:
        if user.handle_str == handle:
            return True
    return False

#Returns User Profile after checking if valid user
def user_profile(token, u_id):
    '''Returns User Profile after checking if valid user'''
    user = database.get_user_object_by_id(u_id)

    if database.get_user_object(token) == "NOT_FOUND":
        raise AccessError(description="Invalid Token")
    elif user == "NOT_FOUND":
        raise InputError(description="User not found")
    else:
        return {'user': user.get_user()}

#Get user from token, make sure the name_first and name_last are valid
#Edit user name_first and name_last to new name_first and name_last
def user_profile_setname(token, name_first, name_last):
    '''Get user from token, make sure the name_first and name_last are valid
        Edit user name_first and name_last to new name_first and name_last
    '''
    if (not name_first.strip() or len(name_first) > 50):
        raise InputError(description="First name needs to be between 1 and 50 characters")
    elif (not name_last.strip() or len(name_last) > 50):
        raise InputError(description="Last name needs to be between 1 and 50 characters")
    else:
        user = database.get_user_object(token)
        user.edit_user_name(name_first, name_last)

    return {}

#Get user from token, make sure that email is valid and has not been used before
#Edit user email to new email
def user_profile_setemail(token, email):
    '''Get user from token, make sure that email is valid and has not been used before
    Edit user email to new email'''
    if not is_valid_email(email):
        raise InputError(description="Email is not valid")
    elif email_already_used(email):
        raise InputError(description="Email has already been used")
    else:
        user = database.get_user_object(token)
        user.edit_user_email(email)

    return {}

#Get user from token, make sure that handle is valid and has not been used before
#Edit user handle to new handle
def user_profile_sethandle(token, handle_str):
    '''Get user from token, make sure that handle is valid and has not been used before
        Edit user handle to new handle'''
    if (len(handle_str) < 2 or len(handle_str) > 20 or handle_str.isspace()):
        raise InputError(description="Handle needs to be between 2 and 50 characters")
    elif handle_already_used(handle_str):
        raise InputError(description="Handle has already been used")
    else:
        user = database.get_user_object(token)
        user.edit_user_handle(handle_str)

    return {}

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''Implementation of user profile upload photo'''
    user = database.get_user_object(token)
    if user == "NOT_FOUND":
        raise AccessError(description="Not a valid user")
    try:
        image = Image.open(urllib.request.urlopen(img_url))
    except (urllib.error.HTTPError, ValueError):
        raise InputError(description="Can not find any image in the given URL")

    #Check x and y are valid
    width, height = image.size
    # Setting the points for cropped image
    left = x_start
    top = y_start
    right = x_end
    bottom = y_end

    #Checking validity of the 'box'
    if(left < 0 or top < 0 or right > width or bottom > height or  right < 0 or bottom < 0):
        raise InputError(description="Coordinates are out side of the uploaded image")
    if(right <= left or bottom <= top):
        raise InputError(description="Coordinates are invalid")
    try:
        #Generate unique url and crop image
        image = image.crop((left, top, right, bottom))
        profile_url = rand_ascii(20)

        des = profile_url + ".jpg"
        profile_image_url = f'http://localhost:{str(SERVER_PORT)}/imgurl/' + des

        user.set_profile_image_url(profile_image_url)

        image.save(f'user_images/{des}', "JPEG", quality=100, optimize=True, progressive=True)
    except OSError:
        raise InputError(description="Not a valid JPG image")
    return {}

def rand_ascii(size):
    '''Creates a random string of ascii characters of given size'''
    # Takes random choices from
    # ascii_letters and digits
    generate_ascii = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])

    return generate_ascii

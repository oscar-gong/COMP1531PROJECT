'''Contains a function that checks if it is a valid email'''
import re

#This function has been copied and adapted from the following link:
#https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
def is_valid_email(email):
    '''checks if it is a valid email'''
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    return re.search(regex, email)

Assumptions file

Testing assumptions
    It is assumed that the state of the backend program does not transfer 
    between tests. For example, an account created in test1 would not exist 
    and must be created again in test2.
    Or even within the *_test.py file for each sub-test function
    Assuming the email which has been registered in one def test_ function will not be affected
    when executing other def test_ function

Function Assumptions:

auth.py

auth_logout_test.py
    
    It is assumed that if the user does not exist, the function would also 
    return false

auth_register_test.py
    
    It is assumed that the requirement for the first and last name to be between 
    1 and 50 chars includes 1 and 50 as valid but does not accept higher than 50
    or less than 1.
    It is also assumed that the email used to sign up does not have to actually 
    exists but as long as it follows the given method in the spec



channel/channels.py:
    
    It is assumed that anyone can invite people into a channel as long as they 
    are in the channel, irrespective of if they are the owner or not
    
    It is assumed that when the owner of a channel leaves the channel without 
    making anyone else an owner before leaving, the channel gets deleted

channel_details_test.py

    It is assumed that this can be run by anyone within the channel irrespective
    of if the channel is public or private

channel_invite_test.py

    It is assumed that this can be run by anyone within the channel irrespective
    of if the channel is public or private. It is also assumed that when the owner
    invites someone into a channel, they are invited with member privileges unless
    the invited person is the owner of Slackr

channel_messages_test.py

    It is assumed that the function will not return anything when an invalid channel ID and user token is inputted, vice versa.
    The integer variable 'start' will never be less than zero.
    It is assumed that when a new channel is created, there are no messages in the channel.

channel_leave_test.py

    It is assumed that the function will not return anything when an invalid channel ID and user token is inputted, vice versa.
    If user is the last one in the channel, the channel will remove itself from the databse.
    If user is the last owner in the channel, the channel will automatically appoint the 1st member(member[0]) as an owner.

channel_join_test.py

    It is assumed that the function will not return anything when an invalid channel ID and user token is inputted, vice versa.
    Assume that if user is an Owner of Slackr then the user will be a channel owner when he joins

channel_addowner_test.py

    It is assumed that the function will return an empty dictionary when ran successfully otherwise None when there's an error.

channel_removeowner_test.py

    It is assumed that the function will return an empty dictionary when ran successfully otherwise None when there's an error.

channels_list_test.py

    When an unauthorised user attempts to run this function, the function will not return anything.

channels_listall_test.py

    Assuming that the system does not have any channels by default.And the 
    number of channels start from 0
    'Invalid_token' is never going to be the valid token
    Assuming when passing a invalid token to the function, InputError is raised

channels_create_test.py

    A channel can not be created twice with the same name and assume InputError
    Assume -100 is never going be valid channel_id
    Assuming 'Invalid_token' is never going to be valid token and assume InputError


message.py:


message_remove_test.py

    Assumimg whenever the channel has a message,the message_id always starts at 1.
    Assuming after the deletion of message in the channel. When transversing the channel, the 
    message can never be found.

message_send_test.py

    Assuming -100 is never going to be valid message_id
    Assuming 'Invalid_token' is never going to be valid token

message_remove_test.py

    Assuming -200 is never going to be valid message_id
    Assuming 'Invalid_token' is never going to be valid token

message_edit_test.py

    Assuming that whenever a user is invited in to the channel , the privilege of the user starts from member until addowner function is called.
    Assuming 'Invalid_token' is never going to be a valid token which will give InputError.
    Assuming -10 is never going to be a valid message_id even if there are some messages in the channel

message_pin_test.py

    Assume that 'Invalid token' is never going to be a valid token
    Assume that -1 is an invalid channel_id, message_id, u_id
    Message pin status can be change by every owner of the channel

message_pin_test.py

    Assume that 'Invalid token' is never going to be a valid token
    Assume that -1 is an invalid channel_id, message_id, u_id
    Message pin status can be change by every owner of the channel

message_react_test.py
    Assume that 'Invalid token' is never going to be a valid token
    Assume that -1 is an invalid channel_id, message_id, u_id
    Every user can react to the post once
    The first person to react to the post does not need to be an Channel owner or message owner
    The u_id list in message reacts is not sorted

message_unreact_test.py
    Assume that 'Invalid token' is never going to be a valid token
    Assume that -1 is an invalid channel_id, message_id, u_id
    A user must react to a post first before he can unreact to the post
    Any user can unreact to the post at any point in time, it does not need to be in order
    The u_id list in messasge reacts is not sorted

message_sendlater_test.py
    Assume that 'Invalid token' is never going to be a valid token
    Assume that -1 is an invalid channel_id, message_id, u_id
    Assume that message_Id of message send in sendlater is gotten when function is called and not when message is sent
    Assume that time of message sent is when the message is sent and not when function is called


other.py:


user_profile_test.py

    Assume that all other functions are working correctly there should be no repeat or missing token/u_id and each token should be unique
    to each u_id, but test case still created for invalid/repeated u_id or token should return InputError
    Assume that similar to slack you click on the photo or name to view profile
    
user_profile_setname_test.py

    Assume that the button to edit a user information is only visible by the user in his profile and only when logged in
    Assume that the you can put symbols and punctuation as valid characters but just "space" is recognise as blank and is not valid
    Assume that repeated names with other user is okay
    Assume that when counting characters space is counted as well but just "space" is not valid
    
user_profile_setemail_test.py

    Assume that the button to edit a user information is only visible by the user in his profile and only when logged in
    Assume that a valid email only means that the it has to pass the regex of what is a possible email and not an actual valid email
    Assume that the function has both the regex to check if it's a valid email as well as a function to check if the email has been used before
    
user_profile_sethandle_test.py

    Assume that the button to edit a user information is only visible by the user in his profile and only when logged in
    Assume that the you can put symbols and punctuation as valid characters but just "space" is recognise as blank and is not valid
    Assume that when counting characters space is counted as well but just "space" is not valid
        
        
user.py:


users_all.py

    Assume that this button is to see all the users in the channel 
    Assume that you have to be logged in to see this button
    Assume that all functions are working and therefore token is unique and valid
    Assume that everyone in the channel can see all the users and you cannot hide anyone
    
search_test.py

    Assume that this is only visible when you are logged in 
    Assume that all functions are working and therefore token is unique and valid
    Assume that the you can put symbols and punctuation as valid characters but just "space" is recognise as blank and is not searchable
    Assume that this function can search a multiple word query but it searches for each word seperately
    and returns all valid search result for each word 

admin.py:

admin_user_permission_test

    Assume all functions are working
    Assume it uses users_all to see all users so they can choose who to set permission
    Assume that if there is only one Global Owner(permission_id = 1) the owner cannot change himself to a member
    this is to ensure that the slack will always have at least one Global Owner
    When changing a user to an owner he automatically becomes an Owner in all channels that he is in if he is not

admin_remove_user_test

    Assume all functions are working
    Assume it uses users_all to see all users so they can choose who to set permission
    Assume that if there is only one Global Owner(permission_id = 1) the owner cannot remove himself
    Assume that that when deleting users it also removes user from channel, removes all his messages and all his reacts

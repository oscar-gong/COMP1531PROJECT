This is a file that explains all the data structures in the project

## Main Database ##
All data stored for the project is going to be stored in a variable called "database".
The "database" variable is an instance of the class serverDatabase which is initiated
within the database.py file. Whenever you are making changes to data, adding or deleting,
make sure you make the changes to the "database" variable and not changing the serverDatabase
class.

# Setup for writing functions #
Since almost all functions require making changes to the database, at the top of your file
you should write the following code:

    from database import database

This also means that you should not at any time within your program create a variable called
"database" or you are instead going to be changing the serverDatabase instance rather than
making a new variable called database.

# Resetting database and pytesting #
There is a function written in the serverDatabase class that full wipes the server database.
To call it run the following code:

    database.reset()

Make sure to put this line of code in the start of every test in your pytests to make sure
the state of the server is reset at every test

# Other database functions #
There are a few other useful functions in the serverDatabase class. Have a look at its structure
in database.py to use.

## Structures within the serverDatabase class ##
Within the main "database" there contains a few properties, more will be added as developement progresses

# registeredUsers #
This is a list containing userEntity objects. It contains all the registered users

# activeUsers #
This is a dictionary where the key is the token of a user and the value is the userEntity object
Whenever a user is logged in, it is added into this dictionary with its key being a freshly generated token
A user is checked to be logged in by searching for the token in the dictionary. When the user is logged out,
its respective key value pair is removed from the dictionary.

## Users ##
When a user is created via auth_register, an instance of the class userEntity is created. This class
contains the user's email, password, name_first, name_last, u_id and handle_str. 

# Token #
A fresh token is created everytime when the user logs in or is registered. It is created by calling the
userEntity.generateToken() function.

# Complying with specs #
On the specs, when they want a user to be outputted, they want a dictionary containing the relevant
user data to be outputted. However, our users are stored as classes rather than dictionaries.
Therefore, a function has been created in the userEntity class called getUser() which returns
a dictionary containing the relevant data.

You can call it like this:

    MyUser.getUser()

## Channels ##
A class has been made for channels called a "channelObject". Feel free to change it as desired or 
discuss further on what should be included in it.

## Message ##
A message object has been created for messages sent. Feel free to make changes to the class upon
discussion with team

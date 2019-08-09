#!/usr/bin/env python3
from irc_client import IrcClient
from database import Database
from character import Character
from game import Game
from conf import *

# creating and initializing client object
IrcClient().connect(HOST, PORT, NAME, OAUTH, CHANNEL)

# creating and initializing database object
Database().initialize()

# A simple dictionary that will get wiped every restart for now ^^
user_db = {}

# The game.
game = Game()

def send(m):
    """
    Sends a message to currently connected chat room as the bot user. This
    function should be used as the underlying code may change
    """

    IrcClient().send_message(m)

def preparse_msg(msg, cmd):
    """
    Does some parsing and returns the command arguments as well as
    the name of the user requesting it
    """

    # Split message by whitespaces
    parts = msg.split()
    # Extract user name
    user = parts[0][1:].split("!")[0]
    # Check if it is a PRIVMSG (chat message) and if it starts with cmd
    if parts[1] != "PRIVMSG" or parts[3] != ":" + cmd:
        return None, user
    # Remove first entries, so that we only have to worry about things after cmd
    return parts[4:], user

def get_character(user):
    """
    Returns the character of the user, or None if there hasn't been created one
    """

    global user_db
    if user in user_db:
        return user_db[user]
    else:
        return None

def add_character(user, char):
    """
    Adds a character in the db for that user
    """

    global user_db
    if user in user_db:
        raise RuntimeError("The old hero has to die first!")
    else:
        user_db[user] = char

def kill_character(user):
    """
    Deletes a character to make place for another
    """

    global user_db
    if user in user_db:
        del user_db[user]
    else:
        raise RuntimeError("There is no hero to kill!")


# IMPORTANT:
# The HANDLERS variable has to contain names of the
# functions that take one string argument and
# return either nothing, or built-in type None
#
# Hondler functions will be given the message, it is
# their duty to determin if the message is important
# for them or not, if not they should return ASAP
# so to not block rest of the handlers from executing

# Section for defining handler functions
def print_msg(msg):
	print(msg)

def help_handler(msg):
    """
    The parser for !help messages to the bot
    """

    # Get the preparsed message
    parts, user = preparse_msg(msg, "!help")
    if parts == None:
        return
    
    # Parse sub category for !help
    if len(parts) == 0:
        send("Available help commands are: do, char and game")
    elif parts[0] == "char":
        send("Help for character creation and development")
    elif parts[0] == "game":
        send("Help for game mechanics")
    elif parts[0] == "do":
        send("Help for do action mechanics")
    else:
        send("@%s There is not help page for %s!" % (user, parts[0]))

def char_handler(msg):
    """
    The parser for !char messages to the bot
    """

    # Get the preparsed message
    parts, user = preparse_msg(msg, "!char")
    if parts == None:
        return
    
    # Get character if there is one available
    char = get_character(user)

    # Parse sub category for !char
    if len(parts) == 0:
        if char == None:
            send("@%s You do not have a character! Please create one first, see '!help char' for more information" % (user))
        else:
            send(char.summary)
    elif parts[0] == "create":
        if len(parts) != 4:
            send("@%s This command must be used like this: '!char create <name> <gender> <class>'!" % (user))
            return
        name = parts[1]
        gender = parts[2].lower()
        class_name = parts[3].lower()
        try:
            add_character(user, Character(name, class_name, gender))
            send("A new hero with the name of %s has entered the stage!" % (name))
        except RuntimeError as e:
            send("@%s %s" % (user, str(e)))
    elif parts[0] == "kill" or parts[0] == "delete":
        try:
            kill_character(user)
            send("%s has passed away!" % (str(char)))
        except RuntimeError as e:
            send("@%s %s" % (user, str(e)))
    else:
        #send("@%s Unknown !char command %s!" % (user, parts[0]))
        send("@%s Unknown !char command [!char %s]!" % (user, parts[0]))

def do_handler(msg):
    """
    The parser for !do messages to the bot
    """

    # Get the preparsed message
    parts, user = preparse_msg(msg, "!do")
    if parts == None:
        return
    
    
    # Get character if there is one available
    char = get_character(user)

    # Parse sub category for !char
    if char == None:
        send("@%s You do not have a character! Please create one first, see '!help char' for more information" % (user))
    else:
        send(char.do(parts))
        
def game_handler(msg):
    """
    The parser for !game messages to the bot
    """

    # Get the preparsed message
    parts, user = preparse_msg(msg, "!game")
    if parts == None:
        return

    # Check for privileges (owner, mod)
    
    # Run game
    #game

# HANDLERS variable has to be below handler functions
HANDLERS = [
	print_msg,
    help_handler,
    char_handler,
    do_handler,
    game_handler
]

# Registering handlers to be used when processing messages
for handler in HANDLERS:
    IrcClient().register_message_handler(handler)

# Loop waiting for user input, other functions can easily
# be implemented, the execution time on those shouldn't
# matter since rest of the program is running in a
# separate thread
while True:
    command: str = input()
    if command == 'exit':
        IrcClient().disconnect()
        break
    elif command:
        send(command)

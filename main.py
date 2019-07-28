#!/bin/python3
from irc_client import IrcClient
from conf import *

# creating and initializing client object
irc_client: IrcClient = IrcClient()
irc_client.connect(HOST, PORT, NAME, OAUTH, CHANNEL)

def send(m):
    global irc_client
    irc_client.send_message(m)

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

def mirror_msg(msg):
    if msg.split()[0] == "mirror":
        send(msg[::-1])

def help_msg(msg):
    # split message by whitespaes
    parts = msg.split()
    # check if it is a PRIVMS (chat message) and if it starts with !help
    if parts[1] != "PRIVMSG" or parts[3] != ":!help":
        return
    # remove first entries, so that we only have to worry about things after !help
    parts = parts[4:]
    
    # parse sub category for !help
    if len(parts) == 0:
        send("Available help commands are: char and game")
    elif parts[0] == "char":
        send("Help for character creation and development")
    elif parts[0] == "game":
        send("Help for game mechanics")
    else:
        send("There is not help page for %s!" % (parts[0]))

# HANDLERS variable has to be below handler functions
HANDLERS = [
	print_msg,
    mirror_msg,
    help_msg
]

# Registering handlers to be used when processing messages
for handler in HANDLERS:
    irc_client.register_message_handler(handler)

# Loop waiting for user input, other functions can easily
# be implemented, the execution time on those shouldn't
# matter since rest of the program is running in a
# separate thread
while True:
    command: str = input()
    if command == 'exit':
        irc_client.disconnect()
        del irc_client
        break
    elif command:
        send(command)

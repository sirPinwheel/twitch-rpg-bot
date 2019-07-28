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

# HANDLERS variable has to be below handler functions
HANDLERS = [
	print_msg,
    mirror_msg
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

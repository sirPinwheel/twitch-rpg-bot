from conf import CHANNEL

def first_char_upper(str):
    """
    This function converts the first char of a string to upper case
    """

    return str[0].upper() + str[1:]

def check_config(H, P, N, O, C):
    """
    Checks if config data format is correct
    """

    if H != 'irc.twitch.tv': return False
    if not isinstance(P, int): return False
    if P != 6697: return False
    if not isinstance(N, str): return False
    if not isinstance(O, str): return False
    if O[:6] != 'oauth:': return False
    if C[0] != '#': return False
    return True

def get_usr(msg: str) -> str:
    """
    Gets user from message string
    """

    end = msg.find('!')
    return msg[1:end]

def get_msg(msg: str) -> str:
    """
    Gets message from message string
    """

    index = msg.find(CHANNEL) + len(CHANNEL) + 2
    return msg[index:]

def is_prefixed(msg: str) -> bool:
    """
    Checks if the message is prefixed with correct command prefix
    """

    if get_msg(msg).find("!") == 0: return True
    return False

from collections import OrderedDict
import re

from util import irc
from util.message import Message
from util.settings import get_setting


hooks = {}
message_hooks = OrderedDict()


def hook(message_type: str):
    """Hook a function to a message type, such as PRIVMSG or JOIN"""
    def wrapper(fn):
        hooks[message_type] = fn
    return wrapper


def msghook(regex):
    """Hook a function to PRIVMSG"""
    def wrapper(fn):
        message_hooks[re.compile(regex, re.IGNORECASE)] = fn
        return fn
    return wrapper


def remember_user(fn):
    """Remember a user"""

    def wrapper(message: Message, match, nick: str):
        print("This feature is not implemented,"
              "but at some point in the future,"
              "the bot will remember who {nick} is")
        return fn(message, match, nick)
    return wrapper


def get_target(message: Message, nick: str) -> str:
    """Figures out what to target. This is because message.target is the bot's own nick in a private message."""
    if message.target == nick:
        return message.nick
    return message.target


def authenticate(fn):
    """Authenticate a user"""
    def wrapper(message: Message, match, nick: str):
        if message.user != get_setting('master'):
            print('authentication failure:', message.user)
            target = get_target(message, nick)
            return irc.chat_message(target, "Not enough privilege")
        print('authorized', message.user)
        return fn(message, match, nick)
    return wrapper

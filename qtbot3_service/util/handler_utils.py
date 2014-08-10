from collections import OrderedDict
import re
import json
import requests
from util import irc
from util.message import Message
from util.settings import get_setting


hooks = {}
message_hooks = OrderedDict()


def hook(message_type: str):
    """Hook a function to a message type, such as PRIVMSG or JOIN"""

    def wrapper(fn):
        hooks[message_type] = fn
        return fn

    return wrapper


def msghook(regex: str):
    """Hook a function to PRIVMSG"""

    def wrapper(fn):
        message_hooks[re.compile(regex, re.IGNORECASE)] = fn
        return fn

    return wrapper


def cmdhook(regex: str):
    """Hook a function to PRIVMSG, but with a prefix defined in settings.json"""

    def wrapper(fn):
        message_hooks[re.compile(get_setting('cmd_prefix') + regex, re.IGNORECASE)] = fn
        return fn

    return wrapper


def store_value(key: str, value) -> bool:
    try:
        url = 'http://127.0.0.1:4001/set/'
        data = json.dumps({'key': key, 'value': value})
        headers = {'content-type': 'application/json'}
        result = json.loads(requests.post(url, headers=headers, data=data).text)

        if result['code'] == 200:
            return result['payload']
        return False

    except Exception as ex:
        print("store_value() exception:", ex)
        return False


def fetch_value(key: str):
    try:
        url = 'http://127.0.0.1:4001/get/'
        data = json.dumps({'key': key})
        headers = {'content-type': 'application/json'}
        result = json.loads(requests.post(url, headers=headers, data=data).text)

        if result['code'] == 200:
            return result['payload']
        return None

    except Exception as ex:
        print("fetch_value() exception:", ex)
        return None


def fetch_all(keyfilter: str="", valuefilter: str=""):
    try:
        url = 'http://127.0.0.1:4001/getall/'
        result = json.loads(requests.get(url).text)

        if result['code'] == 200:
            lines = result['payload']
            if keyfilter or valuefilter:
                lines = {k: v for k, v in lines.items()
                         if k.startswith(keyfilter)
                         and v.startswith(valuefilter)}
            return lines

        return None

    except Exception as ex:
        print("fetch_value() exception:", ex)
        return None


def remember_user(fn):
    """Remember a user"""

    def wrapper(message: Message, nick: str):
        store_value('user_' + message.user, message.nick)
        return fn(message, nick)

    return wrapper


def ignore_self(fn):
    """If the bot did something, make sure it doesn't react to it"""

    def wrapper(message: Message, nick: str):
        if message.nick == nick:
            print("ignoring self")
            return None
        return fn(message, nick)

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


def get_master_nick() -> str:
    return fetch_value('user_' + get_setting('master'))


def is_mentioned(message: Message, nick: str) -> bool:
    lownick = nick.lower()
    lowmsg = message.message.lower()

    if message.target == nick:
        return True

    elif lownick in lowmsg:
        return True

    elif '-' in nick and lownick.split('-', 1)[0] in lowmsg:
        return True

    return False
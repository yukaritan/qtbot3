import json
import time

from util import irc
from util.handler_utils import store_value, fetch_all, get_target, cmdhook
from util.message import Message
from util.settings import get_setting


@cmdhook('tell (?P<recipient>[^\s]+) (?P<message>.+)')
def handle_tell(message: Message, match, nick: str) -> str:

    # get the host for a given nick
    hosts = fetch_all(keyfilter='user_', valuefilter=match['recipient'])

    recipient = match['recipient']

    target = get_target(message, nick)
    if not hosts or recipient not in hosts.values():
        msg = "found no users with the nick " + recipient
        print(msg)
        return irc.chat_message(target, msg)

    print("found hosts", hosts)
    message = json.dumps([message.nick, match['message']])

    for host in (k for k, v in hosts.items() if v == recipient):
        key = "tell_" + host + str(time.time())
        store_value(key, message)

    response = "okay, I will remember that until {nick} says \"{prefix}get told\""
    return irc.chat_message(target, response.format(nick=recipient, prefix=get_setting('cmd_prefix')))


@cmdhook('get told')
def handle_get_told(message: Message, match, nick: str) -> str:

    messages = fetch_all(keyfilter='tell_'+message.user)

    print(messages)
import json
import time

from util import irc
from util.handler_utils import set_value, fetch_all, get_target, cmdhook, unset_value
from qtbot3_common.types.message import Message
from qtbot3_common.util.settings import get_setting


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
        host = host.split('_', 1)[1]
        key = "tell_" + host + str(time.time())
        set_value(key, message)

    response = "okay, I will remember that until {nick} says \"{prefix}get told\""
    return irc.chat_message(target, response.format(nick=recipient, prefix=get_setting('cmd_prefix')))


@cmdhook('get told')
def handle_get_told(message: Message, match, nick: str) -> str:
    messages = fetch_all(keyfilter='tell_' + message.user)

    target = get_target(message, nick)

    if not messages:
        return irc.chat_message(target, "I have no messages for {nick} ;_;".format(nick=message.nick))

    lines = []
    for key, nick_msg in messages.items():
        unset_value(key)
        nick, msg = tuple(json.loads(nick_msg))
        lines.append(message.nick + ': ' + nick + ' said ' + msg)

    return [irc.chat_message(target, line) for line in lines]
from util import irc
from util.handler_utils import message_hooks, cmdhook, get_target
from util.message import Message


@cmdhook('help')
def handle_help(message: Message, match, nick: str):
    print('{nick} asked for help'.format(nick=message.nick))
    response = ', '.join(message_hooks.keys())
    target = get_target(message, nick)
    return irc.chat_message(target, response)

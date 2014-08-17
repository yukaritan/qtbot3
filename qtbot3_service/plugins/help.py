from util import irc
from util.handler_utils import message_hooks, cmdhook, get_target
from qtbot3_common.types.message import Message


@cmdhook('help')
def handle_help(message: Message, match, nick: str):
    """Displays all available commands in regex form. Not very readable at all."""

    print('{nick} asked for help'.format(nick=message.nick))
    response = ', '.join(regex.pattern for regex in message_hooks.keys())
    target = get_target(message, nick)
    return irc.chat_message(target, response)

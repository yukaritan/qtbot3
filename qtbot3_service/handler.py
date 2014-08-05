import util.irc as irc
from util.handler_utils import hook, hooks, message_hooks, remember_user
from util.linetypes import LINE_TYPES
from util.message import Message
from util.settings import get_setting

# noinspection PyUnresolvedReferences
from plugins import commands
# noinspection PyUnresolvedReferences
from plugins import greetings
# noinspection PyUnresolvedReferences
from plugins import rainbow
# noinspection PyUnresolvedReferences
#from plugins import lua


#
#  Hooks
#

@hook('message')
@remember_user
def handle_message(message: Message, nick: str):
    try:
        if message.nick == nick:
            print("ignoring message from self")
            return

        print('message from {nick}: {message}'.format(**message.members))
        for regex, function in message_hooks.items():
            match = regex.match(message.message)
            if match:
                return function(message, match.groupdict(), nick)

    except Exception as ex:
        print('handle_message exeption:', ex)


@hook('server_mode')
def handle_action(message: Message, nick: str):
    print('got server_mode:', message.members)
    return irc.chat_message('NickServ', 'identify ' + get_setting('identify'))


# @hook('notice')
# def handle_notice(message: Message, nick: str):
#     print('notice:', message.members)
#     return '\r\n'.join((irc.chat_message(get_master_nick(), 'I got a notice from %s:' % message.nick),
#                         irc.chat_message(get_master_nick(), message.message)))


@hook('join')
@remember_user
def handle_join(message: Message, nick: str):
    if message.nick == nick:
        return
    print('join:', message.members)
    return irc.chat_message(message.target, 'hai %s! ^__^' % message.nick)


#
#  The only function you should ever have to call
#

def handle(data: str, nick: str) -> Message:
    """nick is the bot's own nick"""
    for name, regex in LINE_TYPES:
        match = regex.match(data)
        if match:
            try:
                # noinspection PyCallingNonCallable
                return hooks[name](Message(**match.groupdict()), nick)
            except KeyError:
                pass

            print('no hooks found for %s.' % name, 'called with:', match.groupdict())

    return ""

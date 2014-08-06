import random
from util import irc
from util.handler_utils import msghook, get_target
from util.message import Message


@msghook('.*h[a]+i.*')
@msghook('.*hey.*')
@msghook('.*hello.*')
def greet(message: Message, match, nick: str) -> str:
    """nick is the bot's own nick"""

    greetings = ['Konnichiwa {nick}~ O-genki desu ka?',
                 'Konnichiwa {nick}~',
                 'Ohayō gozaimasu {nick}!',
                 'Ohayō {nick}!',
                 'Hi {nick}, how are you?',
                 'Nice to see you {nick}. (^_^)']

    greeting = random.choice(greetings)

    lownick = nick.lower()
    lowmsg = message.message.lower()
    if lownick not in lowmsg and ('-' in nick and lownick.split('-', 1)[0] not in lowmsg):
        return
    target = get_target(message, nick)
    return irc.chat_message(target, greeting.format(nick=message.nick))
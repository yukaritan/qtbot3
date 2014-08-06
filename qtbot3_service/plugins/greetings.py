import random
from util import irc
from util.handler_utils import msghook, get_target, hook, remember_user, ignore_self
from util.message import Message


@hook('join')
@remember_user
@ignore_self
def handle_join(message: Message, nick: str):
    print('join:', message.members)
    return irc.chat_message(message.target, 'hai %s! ^__^' % message.nick)


@hook('part')
@hook('quit')
@remember_user
@ignore_self
def handle_part(message: Message, nick: str):
    print('part:', message.members)
    return irc.chat_message(message.target, 'bai %s! ;__;' % message.nick)


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
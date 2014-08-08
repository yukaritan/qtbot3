import random
from util import irc
from util.handler_utils import msghook, get_target, hook, remember_user, ignore_self
from util.message import Message


def prepare_greeting(nick: str) -> str:
    phrase = ['Konnichiwa {nick}~ O-genki desu ka?',
              'Konnichiwa {nick}~',
              'Ohayō gozaimasu {nick}!',
              'Ohayō {nick}!',
              'Hi {nick}, how are you?',
              'Nice to see you {nick}. ^___^',
              'こんにちは {nick}-ちゃん',
              'こんばんは {nick}-ちゃん',
              '元気ですか {nick}-ちゃん',
              'おはよう {nick}-ちゃん']
    phrase = random.choice(phrase)
    return phrase.format(nick=nick)


def prepare_goodbye(nick: str) -> str:
    phrase = ['bai {nick} ;__;',
              'see you later, {nick} ^___^',
              'おやすみなさい',
              'さよなら',
              'ではまた',
              'また明日']
    phrase = random.choice(phrase)
    return phrase.format(nick=nick)


@hook('join')
@remember_user
@ignore_self
def handle_join(message: Message, nick: str):
    print('join:', message.members)
    return irc.chat_message(message.target, prepare_greeting(message.nick))


@hook('part')
@remember_user
@ignore_self
def handle_part(message: Message, nick: str):
    print('part:', message.members)
    target = get_target(message, nick)
    return irc.chat_message(target, prepare_goodbye(message.nick))


@hook('quit')
@remember_user
@ignore_self
def handle_quit(message: Message, nick: str):
    print('quit:', message.members)


@msghook('.*h[a]+i.*')
@msghook('.*hey.*')
@msghook('.*hello.*')
def greet(message: Message, match, nick: str) -> str:
    """nick is the bot's own nick"""
    lownick = nick.lower()
    lowmsg = message.message.lower()
    if lownick in lowmsg or ('-' in nick and lownick.split('-', 1)[0] in lowmsg):
        target = get_target(message, nick)
        return irc.chat_message(target, prepare_greeting(message.nick))


@msghook('.*b[a]+i.*')
@msghook('.*b[y]+[e]+.*')
def goodbye(message: Message, match, nick: str) -> str:
    """nick is the bot's own nick"""
    lownick = nick.lower()
    lowmsg = message.message.lower()
    if lownick in lowmsg or ('-' in nick and lownick.split('-', 1)[0] in lowmsg):
        target = get_target(message, nick)
        return irc.chat_message(target, prepare_goodbye(message.nick))

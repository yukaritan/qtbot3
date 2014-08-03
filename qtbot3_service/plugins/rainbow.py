from util import irc
from util.garbage import colors, repeat
from util.handler_utils import msghook, get_target
from util.message import Message


@msghook('rainbow (?P<message>.*)')
def rainbow(message: Message, match, nick: str) -> str:
    """Color every character"""
    out = ''.join(a + b for a, b in zip(repeat(colors), match['message']))
    return irc.chat_message(get_target(message, nick), out)


@msghook('wrainbow (?P<message>.*)')
def wrainbow(message: Message, match, nick: str) -> str:
    """Color every word"""
    out = ' '.join(a + b for a, b in zip(repeat(colors), match['message'].split(' ')))
    return irc.chat_message(get_target(message, nick), out)

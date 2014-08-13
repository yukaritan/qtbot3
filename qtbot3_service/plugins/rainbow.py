from util import irc
from util.garbage import rainbow as _rainbow, wrainbow as _wrainbow
from util.handler_utils import cmdhook, get_target
from util.message import Message


@cmdhook('rainbow (?P<message>.*)')
def rainbow(message: Message, match, nick: str) -> str:
    """Color every character"""
    return irc.chat_message(get_target(message, nick), _rainbow(match['message']))


@cmdhook('wrainbow (?P<message>.*)')
def wrainbow(message: Message, match, nick: str) -> str:
    """Color every word"""
    return irc.chat_message(get_target(message, nick), _wrainbow(match['message']))

from util import irc
from util.handler_utils import msghook, authenticate
from util.message import Message


@msghook('join (?P<channel>.*)')
@authenticate
def join(message: Message, match, nick: str) -> str:
    """join a channel"""
    channel = match['channel']
    print("got join command from", message.nick, "who wants me to join", channel)
    return irc.join_channel(channel)


@msghook('part (?P<channel>.*)')
@msghook('leave (?P<channel>.*)')
@authenticate
def part(message: Message, match, nick: str) -> str:
    """leave a channel"""
    channel = match['channel']
    print("got part command from", message.nick, "who wants me to leave", channel)
    return irc.part_channel(channel)

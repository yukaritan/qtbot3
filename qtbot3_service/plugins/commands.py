from util import irc
from util.handler_utils import cmdhook, authenticate, msghook, get_target
from qtbot3_common.types.message import Message


@cmdhook('join (?P<channel>.*)')
@authenticate
def join(message: Message, match, nick: str) -> str:
    """join a channel"""
    channel = match['channel']
    print("got join command from", message.nick, "who wants me to join", channel)
    return irc.join_channel(channel)


@cmdhook('part (?P<channel>.*)')
@cmdhook('leave (?P<channel>.*)')
@authenticate
def part(message: Message, match, nick: str) -> str:
    """leave a channel"""
    channel = match['channel']
    print("got part command from", message.nick, "who wants me to leave", channel)
    return irc.part_channel(channel)


@msghook('\\.bots')
def report_as_bot(message: Message, match, nick: str) -> str:
    try:
        target = get_target(message, nick)
        return irc.chat_message(target, "Reporting in! [Python 3] See https://github.com/yukaritan/qtbot3")
    except Exception as ex:
        print(ex)

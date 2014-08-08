from random import choice
from util import irc
from util.handler_utils import msghook, get_target, remember_user, ignore_self
from util.message import Message


def is_mentioned(message: Message, nick: str) -> bool:
    lownick = nick.lower()
    lowmsg = message.message.lower()
    return lownick in lowmsg or ('-' in nick and lownick.split('-', 1)[0] in lowmsg)


@msghook('.*')  # todo: this should be of the lowest possible priority ...and I need to find a way to prioritize hooks
def handle_chat(message: Message, match, nick: str):
    if is_mentioned(message, nick):
        target = get_target(message, nick)

        responses = ["{nick}: you said stuff to or about me! ^__^",
                     "you mentioned me, {nick} ^__^",
                     "{nick} mentioned me! ^__^"]

        return irc.chat_message(target, choice(responses).format(nick=message.nick))


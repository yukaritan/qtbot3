from random import choice
from util import irc
from util.handler_utils import msghook, get_target
from util.irc import is_mentioned
from util.message import Message


@msghook('.*')  # todo: this should be of the lowest possible priority ...and I need to find a way to prioritize hooks
def handle_chat(message: Message, match, nick: str):
    if is_mentioned(message, nick):
        target = get_target(message, nick)

        responses = ["{nick}: you said stuff to or about me! ^__^",
                     "you mentioned me, {nick} ^__^",
                     "{nick} mentioned me! ^__^"]

        return irc.chat_message(target, choice(responses).format(nick=message.nick))


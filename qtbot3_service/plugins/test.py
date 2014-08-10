from util import irc
from util.handler_utils import get_target, fetch_all, get_master_nick, cmdhook
from util.message import Message


@cmdhook('host (?P<nick>.*)')
def get_host(message: Message, match, nick: str) -> str:
    """just parrot the host associated with a nick"""

    print("get_host() was called")

    try:
        target = get_target(message, nick)
        n = match['nick'].strip()
        if ' ' in n:
            n = n.split(' ', 1)[0]

        storage = fetch_all()

        for k, v in storage.items():
            if v == n:
                return irc.chat_message(target, "{v}'s host is {k}".format(k=k.split('_', 1)[1], v=v))
        return irc.chat_message(target, "I don't know {n}'s host yet".format(n=n))

    except Exception as ex:
        print(ex)


@cmdhook('master')
def get_master(message: Message, match, nick: str) -> str:
    target = get_target(message, nick)
    return irc.chat_message(target, "my master is " + get_master_nick() or "unknown to me")


@cmdhook('source')
def get_master(message: Message, match, nick: str) -> str:
    target = get_target(message, nick)
    return irc.chat_message(target, "My source is available at https://github.com/yukaritan/qtbot3")

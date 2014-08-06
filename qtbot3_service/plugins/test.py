from util import irc
from util.handler_utils import msghook, get_target, fetch_all
from util.message import Message


@msghook('host (?P<nick>.*)')
def get_host(message: Message, match, nick: str) -> str:
    """just parrot the host associated with a nick"""

    print("get_host() was called")

    try:
        target = get_target(message, nick)
        n = match['nick']
        storage = fetch_all()

        for k, v in storage.items():
            if v == n:
                return irc.chat_message(target, "{v}'s host is {k}".format(k=k.split('_', 1)[1], v=v))
        return irc.chat_message(target, "I don't know {n}'s host yet".format(n=n))

    except Exception as ex:
        print(ex)
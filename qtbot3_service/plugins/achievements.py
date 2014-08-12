from util import irc
from util.handler_utils import prehook, get_value, set_value, get_target
from util.message import Message


disconnection_ladder = {
    1: "Connection reset by peer",
    5: "Connection reset by beer",
    10: "Connection reset by queer",
    25: "Connection reset by Cher",
    50: "Connection reset by ...deer?",
    100: "Connection reset by ... enough already. I don't know.. Gears?",
    250: "Connection reset 250 times. Seriously?",
    500: "You've lost your connection 500 times. Do you even internet?",
    1000: "One thousand disconnects. A thousand. One, three zeros. Holy shit."
}


@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' PART'
         ' (?P<target>[^\s]+)'
         '( :(?P<message>.*))?')
def achievement_prehook_part(data: str, match: dict, nick: str):
    try:
        key = 'chiev_partcount_' + match['user']
        count = (get_value(key) + 1) or 1
        set_value(key, count)
        print("Achievement progress for {user}: {count}".format(count=count, **match))
    except Exception as ex:
        print("achievement prehook exception:", ex)


@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' PRIVMSG'
         ' (?P<target>[^\s]+)'
         ' :topkek')
@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' JOIN'
         ' (?P<target>[^\s]+)')
def achievement_prehook_part(data: str, match: dict, nick: str):
    try:
        key = 'chiev_partcount_' + match['user']
        count = get_value(key) or 0

        print("Achievement progress for {user}: {count}".format(count=count, **match))

        if count in disconnection_ladder:
            print("Dealt achievement \"" + disconnection_ladder[count] + "\" to", match['nick'])
            target = get_target(Message(**match), nick)
            return irc.chat_message(target, disconnection_ladder[count])
    except Exception as ex:
        print("achievement prehook exception:", ex)



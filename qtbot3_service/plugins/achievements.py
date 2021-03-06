from util import irc
from util.garbage import rainbow
from util.handler_utils import prehook, get_value, set_value, get_target, cmdhook, fetch_all
from qtbot3_common.types.message import Message


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


def get_achievement(message: Message, match: dict, nick: str, count: int) -> str:
    print("Achievement progress for {user}: {count}".format(count=count, **match))
    if count in disconnection_ladder:
        print("Dealt achievement \"" + disconnection_ladder[count] + "\" to", match['nick'])

        if not 'target' in match or match['target'] is None:
            return

        target = get_target(message, nick)
        msg = "{nick} has unlocked an achievement: {desc}"
        msg = rainbow(msg.format(nick=match['nick'], desc=disconnection_ladder[count]))
        return irc.chat_message(target, msg)
    return None


@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' QUIT'
         '( :(?P<message>.*))?')
@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' PART'
         ' (?P<target>[^\s]+)'
         '( :(?P<message>.*))?')
def achievement_prehook_part(message: Message, match: dict, nick: str):
    try:
        key = 'chiev_partcount_' + match['user']

        print("old value:", get_value(key))
        count = (get_value(key) or 0) + 1

        print("new value:", count)

        set_value(key, count)
        return get_achievement(message, match, nick, count)

    except Exception as ex:
        print("achievement prehook exception:", ex)


@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' JOIN'
         ' (?P<target>[^\s]+)')
def achievement_prehook_join(message: Message, match: dict, nick: str):
    try:
        key = 'chiev_partcount_' + match['user']
        count = get_value(key) or 0
        return get_achievement(message, match, nick, count)

    except Exception as ex:
        print("achievement prehook exception:", ex)


@cmdhook('aimbot (?P<nick>[^\s]+)')
def achievement_cheat_codes(message: Message, match: dict, nick: str) -> str:
    fetched = fetch_all(keyfilter='user_', valuefilter=match['nick'])
    target = get_target(message, nick)

    output = []

    for key in fetched:
        user = key.split('_', 1)[1]
        key = 'chiev_partcount_' + user
        count = get_value(key) or 0
        msg = rainbow("%s has disconnected %d times" % (user, count))
        output.append(irc.chat_message(target, msg))

    return output

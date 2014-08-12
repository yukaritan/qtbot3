import json
from util.handler_utils import prehook, get_value, set_value


@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' (PART|PRIVMSG)'
         ' (?P<target>[^\s]+)'
         '( :(?P<message>.*))?')
def achievement_prehook(data: str, match: dict, nick: str):
    try:
        key = 'chiev_partcount_' + match['user']
        raw = get_value(key)
        count = (json.loads(raw) + 1) if raw else 1
        set_value(key, count)
        print("Achievement progress for {user}: {count}".format(count=count, **match))

    except Exception as ex:
        print("achievement prehook exception:", ex)
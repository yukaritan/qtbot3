import json
from util.handler_utils import prehook, get_value, set_value


@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' PART'
         ' (?P<target>[^\s]+)'
         '( :(?P<message>.*))?')
def achievement_prehook(data: str, match: dict, nick: str):
    key = 'chiev_partcount_' + match['host']
    raw = get_value(key)
    count = (json.loads(raw) + 1) if raw else 1
    set_value(key, count)
    print("Achievement progress for {host}: {count}".format(count=count, **match))

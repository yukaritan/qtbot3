from collections import defaultdict

import pygeoip

from util import irc
from util.handler_utils import cmdhook, fetch_all, get_target
from util.message import Message


@cmdhook('country (?P<nick>[^\s]+)')
def handle_country_request(message: Message, match: dict, nick: str) -> str:
    geoip = pygeoip.GeoIP('GeoIP.dat')

    fetched = fetch_all(keyfilter='user_', valuefilter=match['nick'])
    target = get_target(message, nick)

    counter = defaultdict(int)

    for key in fetched:
        host = key.split('@', 1)[1]

        try:
            print("Looking up", host)

            try:
                country = geoip.country_name_by_addr(host)
            except:
                country = geoip.country_name_by_name(host)

            counter[country] += 1

            print("It resolves to", country)
        except Exception as e:
            print(e)

    if not counter:
        return irc.chat_message(target, "{nick} doesn't seem to be on earth".format(nick=match['nick']))

    results = sorted(counter.items(), key=lambda it: it[1])

    message = "{nick}'s hosts resolve to ".format(nick=match['nick'])
    message += ', '.join("{0} {1} times".format(*result) for result in results)

    return irc.chat_message(target, message)

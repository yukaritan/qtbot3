import pygeoip

from util import irc
from util.handler_utils import cmdhook, fetch_all, get_target, get_value
from util.message import Message


@cmdhook('country (?P<nick>[^\s]+)')
def handle_country_request(message: Message, match: dict, nick: str) -> str:
    geoip = pygeoip.GeoIP('GeoIP.dat')

    fetched = fetch_all(keyfilter='user_', valuefilter=match['nick'])
    target = get_target(message, nick)

    output = []

    msg = "{host} is from {country}"
    for key in fetched:
        host = key.split('@', 1)[1]
        country = geoip.country_name_by_addr(host)
        output.append(irc.chat_message(target, msg.format(host=host, country=country)))

    return output

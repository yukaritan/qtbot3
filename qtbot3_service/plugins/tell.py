from util.handler_utils import msghook, store_value, fetch_all
from util.message import Message


@msghook(';tell (?P<nick>[^\s]+) (?P<message>.+)')
def handle_tell(message: Message, match, nick: str) -> str:

    # get the host for a given nick
    hosts = fetch_all(keyfilter='user_', valuefilter=match['nick'])

    print("found hosts", hosts)


    #key = "tell_" + match['nick']


    #store_value()
# This serves as another simple example

import json
import requests
from util import irc
from util.handler_utils import cmdhook, authenticate, msghook, get_target
from qtbot3_common.types.message import Message


@cmdhook('health')
@authenticate
def join(message: Message, match, nick: str) -> str:
    """shows temperatures for now"""
    target = get_target(message, nick)

    try:
        result = json.loads(requests.get("http://localhost:9912/api/temp").text)['payload']

        response = ', '.join("%s: %d" % kv for kv in result.items() if not kv[0] == 'average')
        response += ', average: %d' % result['average']

        return irc.chat_message(target, response)

    except Exception as ex:
        return irc.chat_message(target, str(ex))




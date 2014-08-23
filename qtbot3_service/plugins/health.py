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
        result = json.loads(requests.get("http://localhost:9912/api/temp").text)
        return irc.chat_message(target, str(result['payload']))

    except Exception as ex:
        return irc.chat_message(target, str(ex))




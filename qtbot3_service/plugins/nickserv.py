from util import irc
from util.handler_utils import hook
from util.message import Message
from util.settings import get_setting


@hook('server_mode')
def handle_action(message: Message, nick: str):
    print('got server_mode:', message.members)
    return irc.chat_message('NickServ', 'identify ' + get_setting('identify'))



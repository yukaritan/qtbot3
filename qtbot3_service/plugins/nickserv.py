from util import irc
from util.handler_utils import hook
from qtbot3_common.types.message import Message
from qtbot3_common.util.settings import get_setting


@hook('server_mode')
def handle_action(message: Message, nick: str):
    print('got server_mode:', message.members)
    return irc.chat_message('NickServ', 'identify ' + get_setting('identify'))

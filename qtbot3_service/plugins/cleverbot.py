import cleverbot

from util import irc
from util.handler_utils import msghook, get_target, is_mentioned
from util.message import Message


class CleverbotFactory:
    _cleverbot = None
    _fail = False

    @staticmethod
    def get_instance() -> cleverbot.Cleverbot:
        if not CleverbotFactory._fail and not CleverbotFactory._cleverbot:
            try:
                CleverbotFactory._cleverbot = cleverbot.Cleverbot()
            except ImportError as ex:
                CleverbotFactory._cleverbot = None
                CleverbotFactory._fail = True
                print("Cleverbot integration has failed:", ex)
            except Exception as ex:
                CleverbotFactory._fail = True
                print("Cleverbot integration has failed:", ex)

        return CleverbotFactory._cleverbot


@msghook('.*')  # todo: this should be of the lowest possible priority ...and I need to find a way to prioritize hooks
def handle_chat(message: Message, match, nick: str):

    print("Message from", message.nick,"is being handled by cleverbot integration:", message.message)

    if is_mentioned(message, nick):

        clev = CleverbotFactory.get_instance()
        if not clev:
            print("Could not get instance of cleverbot")
            return

        try:
            response = clev.ask(message.message)
            target = get_target(message, nick)
            return irc.chat_message(target, '{nick}: {response}'.format(nick=message.nick,
                                                                        response=response))
        except cleverbot.CleverbotAPIRejection as ex:
            print("Cleverbot exception:", ex)



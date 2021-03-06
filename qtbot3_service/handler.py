import sys
sys.path.append('..')

import util.irc as irc
from util.handler_utils import hook, hooks, message_hooks, remember_user, get_master_nick, ignore_self, run_prehooks
from util.linetypes import LINE_TYPES
from util.plugin_loader import load_plugin
from qtbot3_common.util.settings import get_setting
from qtbot3_common.types.message import Message


#
# Hooks
#

@hook('message')
@remember_user
@ignore_self
def handle_message(message: Message, nick: str):
    try:
        print('message from {nick}: {message}'.format(**message.members))
        for regex, function in message_hooks.items():
            match = regex.match(message.message)
            if match:
                return function(message, match.groupdict(), nick)

    except Exception as ex:
        print('handle_message exception:', ex)


@hook('notice')
@ignore_self
def handle_notice(message: Message, nick: str):
    print('notice:', message.members)
    return [irc.chat_message(get_master_nick(), 'I got a notice from %s:' % message.nick),
            irc.chat_message(get_master_nick(), message.message)]


#
#  Plugins
#

for plugin in get_setting('plugins'):
    load_plugin(plugin)


#
#  The only function you should ever have to call
#

def handle(data: str, nick: str) -> Message:
    """nick is the bot's own nick"""
    print(data)
    for name, regex in LINE_TYPES:
        match = regex.match(data)
        if match:
            try:
                message = Message(**match.groupdict())
                output = run_prehooks(message, data, nick)

                # noinspection PyCallingNonCallable
                result = hooks[name](message, nick)
                if result:
                    if isinstance(result, list):
                        output += result
                    else:
                        output.append(result)

                return '\r\n'.join(output)

            except KeyError:
                pass

            except Exception as ex:
                print("handle() exception:", ex)

            print('no hooks found for %s.' % name, 'called with:', match.groupdict())
            return

    return None

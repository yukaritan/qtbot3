from util import irc
from util.handler_utils import msghook, authenticate, get_target
from util.message import Message
import lupa


safe_lua_modules = [
    # "coroutine",
    "assert",
    "tostring",
    "tonumber",
    "print",
    # "module",
    "bit",
    # "package",
    "error",
    "debug",
    "rawequal",
    "unpack",
    "pairs",
    "table",
    "next",
    "math",
    "_G",
    "_VERSION",
    "string",
    "type",
    "collectgarbage",
]


def get_sandbox() -> lupa.LuaRuntime:
    # noinspection PyArgumentList
    sandbox = lupa.LuaRuntime(register_eval=False)

    lua_globals = sandbox.globals()
    for module in lua_globals:
        if module not in safe_lua_modules:
            lua_globals[module] = None

    return sandbox


@msghook('eval (?P<code>.*)')
@authenticate
def join(message: Message, match, nick: str) -> str:
    """pull some impressive lua stunts"""

    code = match['code']
    print("received lua code from {nick}: {code}".format(nick=nick, code=code))

    try:
        function = get_sandbox().eval('return ' + code)
        result = '\r\n'.join(str(function()).splitlines())
    except Exception as ex:
        result = '\r\n'.join(str(ex).splitlines())

    target = get_target(message, nick)
    return irc.chat_message(target, result)


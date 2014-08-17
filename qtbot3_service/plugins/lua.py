"""This module is probably dangerous. Use at your own risk."""

import lupa

from util.irc import chat_message
from util.handler_utils import authenticate, get_target, cmdhook
from qtbot3_common.types.message import Message


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


def run_sandbox(template: str, code: str) -> [str]:
    try:
        function = get_sandbox().eval(template.format(code=code))
        return function().splitlines()
    except Exception as ex:
        return str(ex).splitlines()


@cmdhook('evalr (?P<code>.*)')
@authenticate
def lua_evalr(message: Message, match, nick: str) -> str:
    """evaluate a single statement"""
    code = match['code']
    print("received lua code from {nick}: {code}".format(nick=nick, code=code))
    result = run_sandbox('function() return {code} end', code)
    target = get_target(message, nick)
    return [chat_message(target, line) for line in result]


@cmdhook('eval (?P<code>.*)')
@authenticate
def lua_eval(message: Message, match, nick: str) -> str:
    """evaluate a series of statements, but you'll have to return"""
    code = match['code']
    print("received lua code from {nick}: {code}".format(nick=nick, code=code))
    result = run_sandbox('function() {code} end', code)
    target = get_target(message, nick)
    return [chat_message(target, line) for line in result]

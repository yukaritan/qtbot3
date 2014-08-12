from util.handler_utils import prehook


@prehook(':(?P<nick>[^\s]+)'
         '!(?P<user>[^\s]+)'
         ' PRIVMSG'
         ' (?P<target>[^\s]+)'
         ' :(?P<message>.+)')
def achievement_prehook(data: str, match: dict, nick: str):
    print("This got prehooked:", data, match)

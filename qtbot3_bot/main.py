import sys
from qtbot3 import Qtbot3


sys.path.append('..')
# noinspection PyUnresolvedReferences
from qtbot3_service.util.apiresponse import APIResponse
# noinspection PyUnresolvedReferences
from qtbot3_service.util.settings import get_setting


def test():
    nick = get_setting('nick')
    server = get_setting('server')
    port = get_setting('port')

    Qtbot3(nick, server, port).run()


if __name__ == '__main__':
    test()
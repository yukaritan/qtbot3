import sys

sys.path.append('..')
sys.path.append('../qtbot3_service')

from qtbot3 import Qtbot3
from qtbot3_service.util import irc
from qtbot3_service.util.settings import get_setting
from qtbot3_service.util.response import create_response, create_exception

from flask import Flask, request
from threading import Thread


#
#  This won't work at all standalone
#

if __name__ == '__main__':
    print("Please run this behind a WSGI server")
    exit(1)

print("Starting instance")


#
#  Fire up a daemonized qtbot
#

app = Flask(__name__)
qtbot3 = Qtbot3(get_setting('nick'),
                get_setting('server'),
                get_setting('port'))
thread = Thread(target=qtbot3.run, daemon=True)
thread.start()


#
#  Register a few simple ways into the bot
#  so we can do some simple automation
#

@app.route('/say/', methods=['POST'])
def handle_say():
    data = request.get_json()
    try:
        message = irc.chat_message(target=data['target'], message=data['message'])
        qtbot3.send(message)
        return create_response("success")
    except Exception as e:
        return create_exception(e)


@app.route('/join/', methods=['POST'])
def handle_join():
    data = request.get_json()
    try:
        qtbot3.send(irc.join_channel(channel=data['channel']))
        return create_response("success")
    except Exception as e:
        return create_exception(e)


@app.route('/part/', methods=['POST'])
def handle_part():
    data = request.get_json()
    try:
        qtbot3.send(irc.part_channel(channel=data['channel']))
        return create_response("success")
    except Exception as e:
        return create_exception(e)


@app.route('/raw/', methods=['POST'])
def handle_raw():
    data = request.get_json()
    try:
        qtbot3.send(data['raw'])
        return create_response("success")
    except Exception as e:
        return create_exception(e)

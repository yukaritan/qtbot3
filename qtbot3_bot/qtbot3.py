import sys
sys.path.append('..')

from concurrent.futures import ThreadPoolExecutor
import json
import socket
import threading
import requests

# noinspection PyUnresolvedReferences
from qtbot3_common.util.settings import get_setting


class Qtbot3:
    def __init__(self, nick: str, host: str, port: int=6667, ident: str=None, realname: str=None):
        self._host = host
        self._port = port
        self._nick = nick
        self._realname = realname or nick
        self._ident = ident or nick
        self._socket = socket.socket()
        self._channels = []
        self._running = True
        self._debugmode = True
        self._lock = threading.Lock()

    def debug(self, *args, **kw):
        """Prints a debug message if _debugmode is true"""
        if self._debugmode:
            print(*args, **kw)

    def connect(self) -> None:
        """Connects to the server and auths"""
        self._socket.connect((self._host, self._port))
        self.send_many(['NICK %s' % self._nick,
                        'USER %s %s * :%s' % (self._ident,
                                              self._host,
                                              self._realname)])

    def join(self, channel: str) -> None:
        """Joins a channel, listed or not"""
        self.send('JOIN ' + channel)

    def send_many(self, messages: list) -> None:
        """Accepts a list of strings, which it sends them to the server"""
        for message in messages:
            self.send(message)

    def send(self, message: str) -> None:
        """Accepts any string, puts the correct ending on, converts it to bytes, and sends it to the server"""
        with self._lock:
            if not message.startswith('PONG'):
                self.debug(" ->", message)
            self._socket.send((message + "\r\n").encode())

    def say(self, target: str, message: str) -> None:
        """Sends message to target (target can be a user or a channel)"""
        self.send('PRIVMSG %s :%s' % (target, message))

    def read(self) -> [str]:
        """Reads and returns lines, one by one"""
        buffer = b''
        while self._running:
            buffer += self._socket.recv(8192)
            while b'\r\n' in buffer:
                line, buffer = buffer.split(b'\r\n', 1)
                try:
                    line = line.decode().strip()
                    if len(line):
                        yield line.strip()
                except UnicodeDecodeError:
                    self.debug("failed to decode line:", line)
                    pass

    def outsource(self, data: str, nick: str) -> None:
        self.debug("sending to service:", data)
        payload = json.dumps({'nick': nick, 'data': data})
        headers = {'content-type': 'application/json'}
        response = None

        service_host = get_setting('service_host')
        service_port = get_setting('service_port')
        service_url = 'http://{host}:{port}/handle/'.format(host=service_host, port=service_port)

        try:
            response = requests.post(service_url, data=payload, headers=headers).text
            payload = json.loads(response)['payload']
            if payload:
                print("server response:", payload)
                self.send(payload)

        except Exception as ex:
            self.debug("service exception:", ex)
            print('response:', response)

    def run(self):
        print("Starting qtbot3...")
        print("Connecting...")
        self.connect()
        with ThreadPoolExecutor(10) as tpe:
            while self._running:
                for data in self.read():
                    if data.startswith('PING'):
                        self.send('PONG ' + data.split(' ')[1])
                        continue

                    self.debug("incoming:", data)
                    try:
                        # start a new thread for each request we make
                        tpe.submit(self.outsource, data, self.nick)
                    except Exception as ex:
                        self.debug('failed to handle data:', ex)
        print("Exiting")
    #
    # Properties
    #

    @property
    def nick(self) -> str:
        return self._nick

    @property
    def realname(self) -> str:
        return self._realname

    @property
    def name(self) -> str:
        return self._ident

    @property
    def channels(self) -> [str]:
        return self._channels

    @channels.setter
    def channels(self, value) -> None:
        self._channels = value

    @property
    def debugmode(self) -> bool:
        return self._debugmode
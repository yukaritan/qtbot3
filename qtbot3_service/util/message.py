class Message:
    def __init__(self, nick: str=None, target: str=None, user: str=None, message: str=None):
        self._nick = nick
        self._target = target
        self._user = user
        self._message = message

    @property
    def nick(self) -> str:
        return self._nick

    @property
    def target(self) -> str:
        return self._target

    @property
    def user(self) -> str:
        return self._user

    @property
    def message(self) -> str:
        return self._message

    @property
    def members(self) -> dict:
        return {k[1:]: v
                for k, v in self.__dict__.items()
                if not k.startswith('__')
                and k.startswith('_')}
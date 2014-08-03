import json


class APIResponse:
    def __init__(self, payload, error=False, exception=None, code=200):
        self._payload = payload
        self._error = error
        self._exception = exception
        self._code = code

    @staticmethod
    def from_json(raw: str):
        return APIResponse(**json.loads(raw))

    def to_dict(self) -> dict:
        return dict(payload=self._payload,
                    error=self._error,
                    exception=self._exception,
                    code=self._code)

    @property
    def payload(self):
        return self._payload

    @property
    def error(self) -> bool:
        return self._error

    @property
    def exception(self) -> str:
        return self._exception

    @property
    def code(self) -> int:
        return self._code

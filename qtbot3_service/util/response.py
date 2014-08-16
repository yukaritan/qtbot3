from flask import jsonify, make_response
from util.apiresponse import APIResponse


def create_response(payload, error=False, exception=None, code=200):
    response = APIResponse(payload=payload,
                           error=error,
                           exception=str(exception) if exception else None,
                           code=code)
    return make_response(jsonify(response.to_dict()), response.code)


def create_exception(exception, code=500):
    return create_response(payload=None, error=True, exception=exception, code=code)
#!/usr/bin/env python3.4
import sys
sys.path.append('..')

from flask import Flask, request
from qtbot3_common.util.response import create_response
import handler


print("Starting instance")

app = Flask(__name__)


@app.route('/handle/', methods=['POST'])
def handle():
    json = request.get_json()
    response = handler.handle(json['data'], json['nick'])
    return create_response(response)

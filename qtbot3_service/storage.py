#!/usr/bin/env python3.4
import json
from flask import Flask, request
from util.response import create_response, create_exception


class Storage:
    _storage = {}

    @staticmethod
    def get_key(key: str):
        try:
            print('get_key("%s")' % key)
            return create_response(Storage._storage[key])
        except KeyError:
            return create_exception(Exception("Key not found"), 404)

    @staticmethod
    def set_key(key: str, value):
        try:
            print('set_key("%s", "%s")' % (key, value))
            Storage._storage[key] = value
            return create_response(True)
        except Exception as ex:
            return create_exception(ex)

    @staticmethod
    def dump():
        try:
            with open('storage.json', 'w+') as f:
                json.dump(Storage._storage, f)
            return create_response(True)
        except Exception as ex:
            return create_exception(ex)

    @staticmethod
    def load():
        try:
            with open('storage.json', 'r+') as f:
                Storage._storage = json.load(f)
            return create_response(True)
        except Exception as ex:
            return create_exception(ex)

    @staticmethod
    def get_storage():
        return Storage._storage


app = Flask(__name__)


@app.route('/get/', methods=['POST'])
def get_key():
    data = request.get_json()
    return Storage.get_key(data['key'])


@app.route('/set/', methods=['POST'])
def set_key():
    data = request.get_json()
    return Storage.set_key(data['key'], data['value'])


@app.route('/dump/')
def dump_storage():
    return Storage.dump()


@app.route('/load/')
def load_storage():
    return Storage.load()


@app.route('/getall/')
def get_all():
    try:
        storage = Storage.get_storage()
        return create_response(storage)
    except Exception as ex:
        print(ex)
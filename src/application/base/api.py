import flask
import time


def get_json_packet(status=200, data=None):

    if not data:
        data = {}

    return_dict = {
        'meta': {
            'status': status,
            'time': int(time.time())
        },
        'data': data,
    }

    return flask.jsonify(**return_dict)

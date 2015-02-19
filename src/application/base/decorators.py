import functools
import application.base.api


def return_json(func):
    @functools.wraps(func)
    def process_response(*args, **kwargs):
        status, data = func(*args, **kwargs)
        return application.base.api.get_json_packet(status=status, data=data)
    return process_response
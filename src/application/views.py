import flask
import flask_cache
import application
import time
import datetime
import pytz


# Flask-Cache (configured to use App Engine Memcache API)
cache = flask_cache.Cache(application.app)


def home():
    return flask.render_template('index.html', result=None)


def tzhelper():
    tz_string = flask.request.args.get('tz_string')
    date_ints = [a for a in flask.request.args.get('date_ints').split(',')]

    tz = pytz.timezone(tz_string)
    dates = {}
    for date_int in date_ints:
        try:
            y, m, d = parse_date_int(date_int)
        except Exception:
            continue
        dt_utc = datetime.datetime(year=y, month=m, day=d, tzinfo=tz).replace(tzinfo=tz).astimezone(pytz.utc)
        dates[date_int] = int(utc_mktime(dt_utc.timetuple()))

    data = {
        'tz': tz_string,
        'dates': dates,
    }
    return flask.jsonify(**data)


def warmup():
    """
    App Engine warmup handler
    See https://cloud.google.com/appengine/docs/python/config/appconfig?csw=1#Python_app_yaml_Warmup_requests
    """
    return ''


####################################################
def utc_mktime(utc_tuple):
    if len(utc_tuple) == 6:
        utc_tuple += (0, 0, 0)
    return time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))


def parse_date_int(date_int):
    year = int(date_int[:4])
    month = int(date_int[4:6])
    day = int(date_int[6:])
    return year, month, day
####################################################

"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module, 
           which should be kept out of version control.

"""
import secret_keys
# import authomatic.providers.openid
import authomatic.providers.oauth1
import authomatic.providers.oauth2


CONFIG = {
    'tw': {
        # make sure to make the edit to /etc/hosts
        'class_': authomatic.providers.oauth1.Twitter,
        'consumer_key': secret_keys.TW_CONSUMER_KEY,
        'consumer_secret': secret_keys.TW_CONSUMER_SECRET,
    },
    'fb': {
        'class_': authomatic.providers.oauth2.Facebook,
        'consumer_key': secret_keys.FB_APP_ID,
        'consumer_secret': secret_keys.FB_APP_SECRET,
        'scope': ['user_about_me', 'email', 'publish_stream'],
    },
    # 'oi': {
    #     'class_': authomatic.providers.openid.OpenID,
    # }
}


class Config(object):
    # Set secret keys for CSRF protection
    SECRET_KEY = secret_keys.CSRF_SECRET_KEY
    CSRF_SESSION_KEY = secret_keys.SESSION_KEY
    # Flask-Cache settings
    CACHE_TYPE = 'gaememcached'


class Development(Config):
    DEBUG = True
    # Flask-DebugToolbar settings
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CSRF_ENABLED = True


class Testing(Config):
    TESTING = True
    DEBUG = True
    CSRF_ENABLED = True


class Production(Config):
    DEBUG = False
    CSRF_ENABLED = True
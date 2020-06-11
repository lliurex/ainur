import os
import ssl

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    LDAP_REQUIRE_CERT = ssl.CERT_NONE
    LANGUAGES = ['ca_ES_valencia','es','en']
    STATIC_FOLDER = "/static"
    EXPLAIN_TEMPLATE_LOADING = True if os.environ.get('FLASK_ENV') == 'development' else False

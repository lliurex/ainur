from pathlib import Path
import importlib.util as imp_util
from os import listdir
from os.path import join as os_path_join

from flask import Flask, request
from flask_babel import Babel
from flask_login import LoginManager
from flask_ldapconn import LDAPConn
from werkzeug import datastructures

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
ldap = LDAPConn(app)
babel = Babel(app)
login = LoginManager(app)
login.login_view = 'login'

modules_path = os_path_join(app.config['BASE_PATH'],'ainur','modules')
for module_name in listdir(modules_path):
    module_spec = imp_util.spec_from_file_location('ainur.modules.'+module_name, os_path_join(modules_path,module_name,'__init__.py'))
    temp_module = imp_util.module_from_spec(module_spec)
    module_spec.loader.exec_module(temp_module)
    app.register_blueprint(getattr(temp_module,'exportmodule'),url_prefix='/{module_name}'.format(module_name=module_name))

adminmodules_path = os_path_join(app.config['BASE_PATH'],'ainur','adminmodules')
for module_name in listdir(adminmodules_path):
    module_spec = imp_util.spec_from_file_location('ainur.adminmodules.'+module_name, os_path_join(adminmodules_path,module_name,'__init__.py'))
    temp_module = imp_util.module_from_spec(module_spec)
    module_spec.loader.exec_module(temp_module)
    app.register_blueprint(getattr(temp_module,'exportmodule'),url_prefix='/admin/{module_name}'.format(module_name=module_name))



@babel.localeselector
def get_locale():
    list_languages = []
    for x in request.accept_languages:
        if 'ca-valencia' in x[0]:
            x = ('ca_ES_valencia',x[1])
        list_languages.append(x)
    new_list_languages = datastructures.LanguageAccept(list_languages)
    request.accept_languages = new_list_languages
    return new_list_languages.best_match(app.config['LANGUAGES'])

from ainur import models

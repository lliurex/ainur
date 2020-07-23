import os
import importlib.util as imp_util
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from flask_babel import lazy_gettext as _l
from werkzeug.urls import url_parse
import rsa
import base64

from ainur.forms import LoginForm
from ainur import app
from ainur.models import User

@app.route('/')
@app.route('/index')
def index():
    modules_path = os.path.join(app.config['BASE_PATH'],'ainur','modules')
    if os.path.exists(os.path.join(modules_path,'main','__init__.py')):
        module_spec = imp_util.spec_from_file_location('ainur.modules.main', os.path.join(modules_path,'main','__init__.py'))
        temp_module = imp_util.module_from_spec(module_spec)
        module_spec.loader.exec_module(temp_module)
        return temp_module.main()

    return render_template('index.html',title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter('username: '+ form.username.data).first()
        with open('/etc/ainur/ssl/private_key.pem','rb') as fd:        
            privkey = rsa.PrivateKey.load_pkcs1(fd.read())  
        passw = rsa.decrypt(base64.b64decode(form.password.data),privkey)
        if user is None or not user.check_password(passw):
            flash(_l('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    with open('/etc/ainur/ssl/public_key.pem','r') as fd:
        key = fd.read()
    return render_template('login.html', title='Sign In', form=form, publickey=key)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

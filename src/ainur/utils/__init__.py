from flask_login import current_user
from functools import wraps
from flask import render_template
from flask import Blueprint as flask_Blueprint
from ainur import app
import grp
import pwd

def validate_users(users):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args,**kwargs):
            if current_user.is_authenticated and current_user.username not in users:
                return render_template('access_denied.html')
            return function(*args,**kwargs)
        return wrapper
    return inner_function


def validate_groups(groups):
    def inner_function(function):
        @wraps(function)
        def wrapper(*args,**kwargs):
            if current_user.is_authenticated:
                user_groups = [g.gr_name for g in grp.getgrall() if current_user.username in g.gr_mem]
                gid = pwd.getpwnam(current_user.username).pw_gid
                user_groups.append(grp.getgrgid(gid).gr_name)
                if current_user.is_authenticated and len(set(groups) & set(user_groups)) == 0 :
                    return render_template('access_denied.html')
            return function(*args,**kwargs)
        return wrapper
    return inner_function

def dprint (msg='',class_name=''):
    if app.config['ENV'] == 'development':
        try:
            print ("{class_name} {msg}".format(class_name=class_name,msg=msg))
        except Exception as e:
            print("(dprint) Error: {error}".format(error=e))
#def dprint
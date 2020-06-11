from ainur import login, ldap
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.filter('id:' + id).first()


class User(UserMixin, ldap.Entry):

    base_dn = 'ou=People,dc=ma5,dc=lliurex,dc=net'
    object_classes = ['posixAccount']
    id = ldap.Attribute('uidNumber')
    username = ldap.Attribute('uid')
    
    def check_password(self, password):
        return self.authenticate(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

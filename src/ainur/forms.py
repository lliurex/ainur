from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import Input
from wtforms.widgets.core import HTMLString, html_params, escape
from flask_babel import lazy_gettext as _l


class SliderWidget(Input):
    def __call__(self,field,**kargs):
        kargs.setdefault('type','range')
        self.input_type = 'range'
        return super(SliderWidget,self).__call__(field, **kargs)


class SliderField(IntegerField):
    widget = SliderWidget()


class ColorWidget(Input):
    def __call__(self,field,**kargs):
        kargs.setdefault('type','color')
        self.input_type = 'color'
        return super(ColorWidget,self).__call__(field, **kargs)


class ColorField(StringField):
    widget = ColorWidget()


class LoginForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))
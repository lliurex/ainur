from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

exportmodule = Blueprint('exportmodule', __name__,template_folder='templates')

@exportmodule.route('/', defaults={'page': 'index'})
@exportmodule.route('/<page>')
def show(page):
    try:
        return render_template('pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
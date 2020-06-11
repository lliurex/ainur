from flask import render_template, abort, Blueprint
from jinja2 import TemplateNotFound

exportmodule = Blueprint('admin_exportmodule', __name__,template_folder='templates')

@exportmodule.route('/', defaults={'page': 'index'})
@exportmodule.route('/<page>')
def show(page):
    try:
        return render_template('admin/pages/%s.html' % page)
    except TemplateNotFound:
        abort(404)
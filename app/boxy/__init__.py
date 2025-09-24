from flask import Blueprint

boxy = Blueprint('boxy', __name__, template_folder='templates', static_folder='static',
    static_url_path='/boxy/static')

from . import views_boxies
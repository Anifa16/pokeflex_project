from flask import Blueprint

post = Blueprint('post', __name__, template_folder='post_templates', url_prefix='/post')

from . import routes
from flask import Blueprint

# Initialize routes blueprint
routes = Blueprint('routes', __name__, url_prefix='/')

# Import route modules
from . import route1, route2

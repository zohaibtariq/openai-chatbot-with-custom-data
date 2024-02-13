# /app/__init__.py

from flask import Flask

# Initialize Flask application
app = Flask(__name__)

# Import routes
from app.routes import routes

app.register_blueprint(routes)

# Import views
from app.views import views

app.register_blueprint(views)

# Set up template directory
app.template_folder = 'templates'

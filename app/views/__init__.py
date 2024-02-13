# /app/views/__init__.py
from app import app
from flask import Blueprint
views = Blueprint('views', __name__)
from . import view1, view2

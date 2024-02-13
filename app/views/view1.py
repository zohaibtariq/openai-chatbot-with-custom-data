from app.services.logic1 import process_data1
from flask import render_template
from . import views


# import os

# used for html view based pages

@views.route('/')
def index():
    # return os.getenv("MY_VARIABLE")
    data = process_data1("Home data")
    return render_template('chatbot.html', data=data)

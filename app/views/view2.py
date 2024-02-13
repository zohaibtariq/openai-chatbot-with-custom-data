# from . import app
from app.services.logic2 import process_data2
from flask import render_template
from . import views


# used for html view based pages

# @views.route('/other')
# def other_view():
#     data = process_data2("Some other data")
#     return render_template('other_template.html', data=data)

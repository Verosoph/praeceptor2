from flask import Blueprint
from flask import render_template

mod = Blueprint('home', __name__,template_folder='templates', static_folder='static')

@mod.route('/')
def home():
    return render_template('home.html')
from flask import Blueprint
from flask import render_template
#from myapp.auth.view_auth import is_logged_in
from ..auth.view_auth import is_logged_in

mod = Blueprint('desk', __name__,template_folder='templates')
@mod.route('/desk')
@is_logged_in
def desk():
    return render_template('desk.html')
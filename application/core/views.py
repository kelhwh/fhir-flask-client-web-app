from flask import render_template, Blueprint

from flask_login import login_required

core = Blueprint('core', __name__)

@core.route('/', methods=['GET'])
def welcome():
    return render_template ('welcome.html')

@login_required
@core.route('/', methods=['GET'])
def main():
    return render_template ('main.html')

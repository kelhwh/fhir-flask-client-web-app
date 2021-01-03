from flask import render_template, Blueprint
from flask_login import login_required

core_bp = Blueprint('core_bp', __name__)

@core_bp.route('/', methods=['GET'])
def welcome():
    return render_template ('welcome.html')

@login_required
@core_bp.route('/', methods=['GET'])
def main():
    return render_template ('main.html')

@core_bp.app_errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

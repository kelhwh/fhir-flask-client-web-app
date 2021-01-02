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

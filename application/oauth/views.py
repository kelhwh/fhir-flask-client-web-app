from flask import render_template, Blueprint, redirect, url_for,flash, request
from flask_login import login_user, current_user, logout_user
from application import db
from application.models import UserModel
from application.users.forms import LoginForm, RegistrationForm
from application.fhir.search import ResourceFinder
from application.fhir.connect import smart

oauth_bp = Blueprint(
    'oauth_bp',
    __name__,
    url_prefix='/oauth'
)

@oauth_bp.route('/<service>', methods=['GET'])
def index(service):
    # url of authorize endpoint with params appended
    url = smart.authorize_url

    return redirect(url, 302)

@oauth_bp.route('/<service>/callback')
def oauth2_callback(service):
    print(service)

    smart.handle_callback(request.url)
    if smart.ready:
        flash(f'Successfully authorized by {service.upper()}! Welcome, {smart.human_name(smart.patient.name[0])}!')
    else:
        flash(f'Authorization Failed! Please try again.')


    return redirect(url_for('core_bp.welcome'))

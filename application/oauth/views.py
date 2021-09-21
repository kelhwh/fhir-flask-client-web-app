from flask import render_template, Blueprint, redirect, url_for,flash, request
from flask_login import login_user
from application import db
from application.models import UserModel
from application.fhir.search import ResourceFinder
from application.fhir.connect import smart
import uuid
from datetime import date

oauth_bp = Blueprint(
    'oauth_bp',
    __name__,
    url_prefix='/oauth',
    template_folder='templates/oauth'
)

@oauth_bp.route('/', methods=['GET'])
def index():

    return render_template('index.html')

@oauth_bp.route('/<service>', methods=['GET'])
def redirect_to_auth(service):
    # url of authorize endpoint with params appended
    url = smart.authorize_url

    return redirect(url, 302)

@oauth_bp.route('/<service>/callback')
def oauth2_callback(service):
    print(service)

    smart.handle_callback(request.url)

    if smart.ready:
        patient = smart.patient
        print(smart.patient_id)
        print(smart.server.auth.access_token)

        user = UserModel.query.filter_by(patient_id=smart.patient_id).first()
        if user:
            pass
        else:
            user = UserModel(
                given_name = patient.name[0].given[0],
                family_name =  patient.name[0].family,
                date_of_birth = date.fromisoformat(patient.birthDate.isostring),
                identifier_system = None,
                identifier_value = None,
                oauth_server = service,
                patient_id = smart.patient_id,
                email = None,
                password = uuid.uuid1().__str__() #to be deprecated in oauth version
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)

        flash(f'Successfully authorized by {service.upper()}! Welcome, {smart.human_name(smart.patient.name[0])}!')

    else:
        flash(f'Authorization Failed! Please try again.')


    return redirect(url_for('core_bp.welcome'))

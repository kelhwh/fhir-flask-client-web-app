from flask import render_template, Blueprint, redirect, url_for,flash, request
from flask_login import login_user, logout_user
from application import db
from application.models import UserModel
from application.fhir.search import ResourceFinder
from application.fhir.connect import connector
import uuid
from datetime import date

oauth_bp = Blueprint(
    'oauth_bp',
    __name__,
    url_prefix='/oauth',
    template_folder='templates/oauth'
)


@oauth_bp.route('/<connection_type>', methods=['GET'])
def index(connection_type):

    return render_template('index.html', connection_type=connection_type)

@oauth_bp.route('/<service>/<connection_type>', methods=['GET'])
def redirect_to_auth(service, connection_type):
    """Direct to the authorize page based on selected parameters.
    """

    connector.connect(service=service, connection_type=connection_type)

    # url of authorize endpoint with params appended
    if connection_type == 'source':
        url = connector.source_client.authorize_url
    elif connection_type == 'target':
        url = connector.target_client.authorize_url

    print(url)
    print(connector.client_dict)

    return redirect(url, 302)

@oauth_bp.route('/reset', methods=['GET'])
def reset():
    #Reset all connected FHIR clients
    connector.reset()

    #Logout flask login
    logout_user()

    flash("You've now logged out.")
    return redirect(url_for('core_bp.welcome'))

@oauth_bp.route('/<service>/callback')
def oauth2_callback(service):
    """An intermediate step to show banner and add user into app database once OAuth is successfully passed.
    """

    client = connector.client_dict[service]
    client.handle_callback(request.url)

    if client.ready:
        patient = client.patient
        #print(client.patient_id)
        #print(client.server.auth.access_token)

        user = UserModel.query.filter_by(patient_id=client.patient_id).first()
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
                patient_id = client.patient_id,
                email = None,
                password = uuid.uuid1().__str__() #to be deprecated in oauth version
            )
            db.session.add(user)
            db.session.commit()

        login_user(user)

        flash(f'Successfully authorized by {service.upper()}! Welcome, {client.human_name(client.patient.name[0])}!')

    else:
        flash(f'Authorization Failed! Please try again.')


    return redirect(url_for('core_bp.main'))

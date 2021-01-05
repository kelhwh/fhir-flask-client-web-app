from flask import render_template, Blueprint
from flask_login import current_user, login_required
from application.fhir.search import ResourceFinder
from contextlib import suppress


profile_bp = Blueprint(
    'profile_bp',
    __name__,
    url_prefix='/profile'
)


@profile_bp.route('/', methods=['GET'])
@login_required
def profile():

    PatientFinder = ResourceFinder.build('Patient')
    patient = PatientFinder.find_by_identifier(
        current_user.identifier_system,
        current_user.identifier_value,
        first=True
    )

    profile={}
    with suppress(TypeError):
        profile['title'] = patient.name[0].prefix[0]
        profile['contact'] = "{}: {} ({})".format(
            patient.telecom[0].system,
            patient.telecom[0].value,
            patient.telecom[0].use
        )
        profile['address'] = ", ".join([
            patient.address[0].city,
            patient.address[0].state,
            patient.address[0].postalCode,
            patient.address[0].country
        ])
        profile['language'] = patient.communication[0].language.text

    return render_template('profile.html', profile=profile)

from flask import render_template, Blueprint, session, flash, redirect, url_for
from flask_login import current_user, login_required
from fhirclient.models.patient import Patient
from contextlib import suppress
from application.fhir.connect import connector
from application.fhir.search import ResourceFinder
from application.profile.forms import EditProfileForm
from application.oauth.utils import oauth_required

profile_bp = Blueprint(
    'profile_bp',
    __name__,
    url_prefix='/profile'
)


@profile_bp.route('/', methods=['GET'])
@oauth_required
def profile():
    smart = connector.source_client
    PatientFinder = ResourceFinder.build('Patient', smart.server)
    patient = PatientFinder.find_by_id(smart.patient_id, first=True)

    profile={}
    with suppress(TypeError):
        profile['title'] = patient.as_json().get('name', [{}])[0].get('prefix', [None])[0]# patient.name[0].prefix[0]
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
        profile['city'] = patient.address[0].city
        profile['state'] = patient.address[0].state
        profile['postalcode'] = patient.address[0].postalCode
        profile['country'] = patient.address[0].country
        profile['language'] = patient.communication[0].language.text

        session['profile'] = profile

    return render_template('profile.html', profile=profile, smart=smart)

@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    try:
        session['profile']
    except KeyError:
        return redirect(url_for('profile_bp.profile'))

    form = EditProfileForm()

    smart = connector.source_client
    PatientFinder = ResourceFinder.build('Patient', smart.server)
    patient = PatientFinder.find_by_id(
        current_user.patient_id,
        first=True
    )

    if form.validate_on_submit():
        city = form.city.data
        state = form.state.data
        postalcode = form.postalcode.data
        country = form.country.data

        patient.address[0].city = city
        patient.address[0].state = state
        patient.address[0].postalCode = postalcode
        patient.address[0].country = country

        updated_patient_dict = patient.update()

        if updated_patient_dict:
            flash("Your profile has been updated successfully!")
            return redirect(url_for('profile_bp.profile'))

    return render_template('edit.html', form=form, profile=session['profile'])

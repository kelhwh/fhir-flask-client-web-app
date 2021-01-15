from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from application.fhir.connect import smart
from application.fhir.search import ResourceFinder
from datetime import datetime

medications_bp = Blueprint(
    'medications_bp',
    __name__,
    url_prefix='/medications'
)

@medications_bp.route('/timeline')
@login_required
def timeline():
    MedicationRequestFinder = ResourceFinder('MedicationRequest', smart.server)

    resouce_list = MedicationRequestFinder.find_by_patient(current_user.patient_id).resource_list()

    medications = []
    for m in resouce_list:
        m = m.as_json()

        dict = {}
        dict['medication_name'] = m.get('medicationCodeableConcept', {}).get('text')
        dict['pratitioner'] = m.get('requester', {}).get('agent')
        dict['reason'] = m.get('reasonReference')[0].get('reference') if m.get('reasonReference') else 'Not provided'
        dict['date'] = datetime.fromisoformat(m.get('authoredOn')).date().__str__()

        medications.append(dict)

    return render_template('timeline.html', medications=medications)

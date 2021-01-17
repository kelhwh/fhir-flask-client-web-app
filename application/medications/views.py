from flask import render_template, Blueprint, redirect, url_for
from flask_login import current_user, login_required
from fhirclient.models import condition, practitioner
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
        #dict['pratitioner_name'] = m.get('requester', {}).get('agent').get('reference')
        #dict['reason'] = m.get('reasonReference', [{}])[0].get('reference')
        dict['date'] = datetime.fromisoformat(m.get('authoredOn')).date().__str__()
        if m.get('requester', {}).get('agent', {}).get('reference') is not None:
            resource = practitioner.Practitioner.read_from(m.get('requester', {}).get('agent').get('reference'), smart.server)
            dict['practitioner_name'] = smart.human_name(resource.name[0])

        if m.get('reasonReference', [{}])[0].get('reference') is not None:
            resource = condition.Condition.read_from(m.get('reasonReference', [{}])[0].get('reference'), smart.server)
            dict['reason'] = resource.code.text

        medications.append(dict)
        medications = [i for i in sorted(medications, key=lambda item: item['date'], reverse=True)]

    return render_template('timeline.html', medications=medications)


@medications_bp.route('/grid')
def grid():
    return render_template('grid.html')

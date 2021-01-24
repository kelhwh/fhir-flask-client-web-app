from flask import render_template, Blueprint, redirect, url_for, request
from flask_login import current_user, login_required
from fhirclient.models import condition, practitioner
from application.fhir.connect import smart
from application.fhir.search import ResourceFinder
from datetime import datetime, timedelta
import pandas as pd

medications_bp = Blueprint(
    'medications_bp',
    __name__,
    url_prefix='/medications',
    template_folder='templates/medications'
)

@medications_bp.route('/list')
@login_required
def list():
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
        medications = [m for m in sorted(medications, key=lambda item: item['date'], reverse=True)]

    return render_template('list.html', medications=medications)


@medications_bp.route('/grid', methods=['GET'])
def grid():
    search_date = request.args.get('search_date') or '2014-01-25'
    search_date = datetime.fromisoformat(search_date).date()
    start = search_date - timedelta(days = 15)
    end = search_date + timedelta(days = 15)
    date_range = pd.date_range(start=start,end=end)

    search_params = [
        ('patient', str(current_user.patient_id)),
        ('effective-time', 'ge' + start.__str__()),
        ('effective-time', 'le' + end.__str__())
    ]

    MedicationAdministrationFinder = ResourceFinder.build('MedicationAdministration', smart.server)
    resouce_list = MedicationAdministrationFinder.find(search_params=search_params).resource_list()
    print(resouce_list)
    medications = []
    for m in resouce_list:
        m = m.as_json()

        dict = {}
        dict['medication_name'] = m.get('medicationCodeableConcept', {}).get('text')
        dict['start_position'] = (datetime.fromisoformat(m.get('effectivePeriod').get('start')).date() - start).days + 1
        dict['end_position'] = (datetime.fromisoformat(m.get('effectivePeriod').get('end')).date() - start).days + 2

        medications.append(dict)

    return render_template('grid.html', medications=medications, search_date=search_date, start=start, end=end, date_range=date_range)

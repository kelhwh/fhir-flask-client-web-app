from flask import render_template, Blueprint, redirect, url_for, request
from fhirclient.models import condition, practitioner
from application.fhir.connect import connector
from application.fhir.search import ResourceFinder
from application.oauth.utils import oauth_required
from datetime import datetime, timedelta
import pandas as pd


medications_bp = Blueprint(
    'medications_bp',
    __name__,
    url_prefix='/medications',
    template_folder='templates/medications'
)

@medications_bp.route('/list')
@oauth_required
def list():
    smart=connector.source_client
    MedicationRequestFinder = ResourceFinder('MedicationRequest', smart.server)

    result = MedicationRequestFinder.find_by_patient(smart.patient_id)
    resource_list = [item for item in result.resource_list() if item.resource_type==MedicationRequestFinder.resource_type]

    medications = []
    for m in resource_list:
        m = m.as_json()

        dict = {}

        # This seems to be Epic specific format, normally it would be:
        # dict['medication_name'] = m.get('medicationCodeableConcept', {}).get('text')
        dict['medication_name'] = m.get('medicationReference', {}).get('display')

        dict['date'] = m.get('authoredOn')
        if m.get('requester', {}).get('agent', {}).get('reference') is not None:
            resource = practitioner.Practitioner.read_from(m.get('requester', {}).get('agent').get('reference'), smart.server)
            dict['practitioner_name'] = smart.human_name(resource.name[0])

        if m.get('reasonReference', [{}])[0].get('reference') is not None:
            resource = condition.Condition.read_from(m.get('reasonReference', [{}])[0].get('reference'), smart.server)
            dict['reason'] = resource.code.text

        medications.append(dict)
        medications = [m for m in sorted(medications, key=lambda item: item['date'], reverse=True)]

    return render_template('list.html', medications=medications, smart=smart)


@medications_bp.route('/grid', methods=['GET'])
@oauth_required
def grid():
    smart=connector.source_client
    
    search_date = request.args.get('search_date') or '2014-01-25'
    search_date = datetime.fromisoformat(search_date).date()
    start = search_date - timedelta(days = 15)
    end = search_date + timedelta(days = 15)
    date_range = pd.date_range(start=start,end=end)

    search_params = [
        ('patient', str(smart.patient_id)),
        ('effective-time', 'ge' + start.__str__()),
        ('effective-time', 'le' + end.__str__())
    ]

    MedicationAdministrationFinder = ResourceFinder.build('MedicationAdministration', smart.server)
    result = MedicationAdministrationFinder.find(search_params=search_params)

    resource_list = [item for item in result.resource_list() if item.resource_type==MedicationAdministrationFinder.resource_type]

    medications = []
    for m in resource_list:
        m = m.as_json()

        dict = {}
        dict['medication_name'] = m.get('medicationCodeableConcept', {}).get('text')
        dict['start_position'] = (datetime.fromisoformat(m.get('effectivePeriod').get('start')).date() - start).days + 1
        dict['end_position'] = (datetime.fromisoformat(m.get('effectivePeriod').get('end')).date() - start).days + 2

        medications.append(dict)

    return render_template(
        'grid.html',
        medications=medications,
        search_date=search_date,
        start=start,
        end=end,
        date_range=date_range,
        smart=smart
    )

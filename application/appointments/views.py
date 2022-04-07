from flask import render_template, Blueprint, request
from application.fhir.search import ResourceFinder
from application.fhir.connect import connector
from contextlib import suppress
from application.oauth.utils import oauth_required

ROWS_PER_PAGE = 10

appointments_bp = Blueprint(
    'appointments_bp',
    __name__,
    url_prefix='/appointments'
)


@appointments_bp.route('/list', methods=['GET'])
@oauth_required
def list():
    smart=connector.source_client

    page = request.args.get('page', 1, type=int)

    OrganizationFinder = ResourceFinder.build('Organization', smart.server)
    EncounterFinder = ResourceFinder.build('Encounter', smart.server)

    result = EncounterFinder.find_by_patient(smart.patient_id, batch_size=ROWS_PER_PAGE, page=page)
    appointments_list = [item for item in result.resource_list() if item.resource_type==EncounterFinder.resource_type]

    max_page = ((result.total or 0) // ROWS_PER_PAGE) + 1
    appointments = []


    for appointment in appointments_list:
        try:
            ref = appointment.serviceProvider.reference.split("/")[-1]
            id = ref.split("/")[-1]
            provider = OrganizationFinder.find_by_id(id, first=True)
            provider_name = provider.name
        except:
            provider_name = None

        dict = {}
        with suppress(TypeError):
            dict['time'] = appointment.period.start.isostring
        with suppress(TypeError):
            dict['type'] = appointment.type[0].text
        with suppress(TypeError):
            dict['reason'] = appointment.reason[0].coding[0].display
        with suppress(TypeError):
            dict['provider'] = provider_name
        with suppress(TypeError):
            dict['id'] = appointment.id
        appointments.append(dict)

    return render_template(
        'appointments.html'
        , appointments=appointments
        , max_page=max_page
        , current_page=page
        , smart=smart
    )

from flask import render_template, Blueprint, request
from flask_login import current_user, login_required
from application.fhir.search import ResourceFinder
from contextlib import suppress

ROWS_PER_PAGE = 10

appointments_bp = Blueprint(
    'appointments_bp',
    __name__,
    url_prefix='/appointments'
)


@appointments_bp.route('/list', methods=['GET'])
@login_required
def list():
    page = request.args.get('page', 1, type=int)

    OrganizationFinder = ResourceFinder.build('Organization', batch_size=1)
    EncounterFinder = ResourceFinder.build('Encounter', batch_size=ROWS_PER_PAGE)

    result = EncounterFinder.find_by_patient(current_user.patient_id, page=page)
    appointments_list = result.resource_list()

    max_page = ((result.total or 0) // ROWS_PER_PAGE) + 1
    appointments = []


    for appointment in appointments_list:
        try:
            ref = appointment.serviceProvider.reference.split("/")[-1]
            id = ref.split("/")[-1]
            provider = OrganizationFinder.find_by_id(id)
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
        appointments.append(dict)

    return render_template(
        'appointments.html'
        , appointments=appointments
        , max_page=max_page
        , current_page = page
    )

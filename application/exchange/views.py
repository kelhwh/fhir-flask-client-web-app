from flask import flash, Blueprint, redirect, request, url_for
from application.fhir.search import ResourceFinder
from application.fhir.connect import connector
from application.oauth.utils import oauth_required


exchange_bp = Blueprint(
    'exchange_bp',
    __name__,
    url_prefix='/exchange'
)

@exchange_bp.route('/<resource_type>/<id>')
def exchange(resource_type, id):
    """Send specific FHIR resource from source client to target client.
    """
    path = resource_type

    if connector.target_client is None:
        return redirect(url_for('oauth_bp.index', connection_type='target'))
    else:
        pass

    finder = ResourceFinder.build(resource_type, server=connector.source_client.server)
    resource = finder.find_by_id(id, first=True)

    #Change subject to target client patient reference
    resource.subject.reference = "Patient/{}".format(connector.target_client.patient_id)

    #Post resource to targer server: https://base_uri/resource_type
    response = connector.post_to_target(resource_type, resource.as_json())

    if response.status_code < 400:
        flash("Successfully shared to {}!".format(connector.target_client.server.base_uri))
    elif 401 == response.status_code:
        flash("Data sharing failed! Unauthorized request.")
    elif 403 == response.status_code:
        flash("Data sharing failed! Permission denied.")
    elif 405 == response.status_code:
        flash("Data sharing failed! Not allowed to send data into {}.".format(connector.target_client.server.base_uri))
    else:
        flash("Data sharing failed! Something went wrong.")

    return redirect(request.referrer)

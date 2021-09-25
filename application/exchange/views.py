from flask import flash, Blueprint, redirect, request, url_for
from application.fhir.search import ResourceFinder
from application.fhir.connect import connector


exchange_bp = Blueprint(
    'exchange_bp',
    __name__,
    url_prefix='/exchange'
)

@exchange_bp.route('/<resource_type>/<id>')
def exchange(resource_type, id):
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
    res = connector.target_client.server.post_json(path, resource.as_json())
    print(res.content)
    if res.content:
        flash("Successfully shared to {}!".format(connector.target_client.server.base_uri))

    return redirect(request.referrer)

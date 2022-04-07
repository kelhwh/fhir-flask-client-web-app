from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch
import yaml
import json

class ClientConnector():
"""An object to host two FHIR client an perform data exchange.
"""
    def __init__(self, *args, **kwargs):
        self.source_client = None
        self.target_client = None
        self.client_dict = dict()

        with open('application/fhir/server_config.yml') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.server_config = config

    def connect(self, service, connection_type):
        settings = self.server_config.get(service)

        if connection_type=='source':
            self.source_client = client.FHIRClient(settings=settings)
            self.client_dict[service] = self.source_client
        elif connection_type=='target':
            self.target_client = client.FHIRClient(settings=settings)
            self.client_dict[service] = self.target_client

    def reset(self):
        self.__init__()

    def post_to_target(self, resource_type, resource_json):

        url = '/'.join([self.target_client.server.base_uri, resource_type])
        headers = {
            'Accept': 'application/fhir+json',
            'Accept-Charset': 'UTF-8',
            'Content-Type': 'application/fhir+json'
        }
        if not self.target_client.server.auth is not None and self.target_client.server.auth.can_sign_headers():
            headers = self.target_client.server.auth.signed_headers(headers)

        # perform the request but intercept 401 responses, raising our own Exception
        res = self.target_client.server.session.post(url, headers=headers, data=json.dumps(resource_json))
        return res

connector = ClientConnector()
smart = connector.source_client

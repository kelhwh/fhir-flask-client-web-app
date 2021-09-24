from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch
import yaml


class ClientConnector():
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

connector = ClientConnector()
smart = connector.source_client

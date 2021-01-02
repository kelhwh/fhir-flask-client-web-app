from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch

settings = {
    'app_id': 'my_web_app',
    'api_base':  'http://hapi.fhir.org/baseDstu3/'
}

smart = client.FHIRClient(settings=settings)

from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch

settings = {
    'app_id': '8ba7dd62-013b-4c3f-94b2-2f10004a8dde',
    'redirect_uri': 'http://127.0.0.1:5000/oauth/epic/callback',
    'api_base': 'https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/STU3/' #'https://launch.smarthealthit.org/v/r3/sim/eyJrIjoiMSIsImIiOiIyNjc1NjEifQ/fhir'
}

smart = client.FHIRClient(settings=settings)


# https://launch.smarthealthit.org/v/r3/sim/eyJrIjoiMSIsImIiOiIyNjc1NjEifQ/fhir
# 267561

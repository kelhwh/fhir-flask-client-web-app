from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch

settings = {
    'app_id': 'my_web_app',
    'api_base':  'http://hapi.fhir.org/baseDstu3/'#'https://fhir-open-api-dstu2.smarthealthit.org'
}

smart = client.FHIRClient(settings=settings)

from fhirclient.models import patient as p

struct = {'identifier':'http://hl7.org/fhir/sid/us-ssn|999-45-3776'}
#patient = p.Patient.read('1349276', smart.server)
search = p.Patient.where(struct=struct)
patient = search.perform(smart.server).entry[0].resource
patient = search.perform_resources(smart.server)[0]

print(patient.birthDate.isostring)

print(patient.id)

print(smart.human_name(patient.name[0]))
print(search.resource_type.resource_type)


# import fhirclient.models.encounter as encounter
# #search = p.Procedure.where(struct={'subject': 'hca-pat-1', 'status': 'completed'})
# search = encounter.Encounter.where(struct={'subject':'1349276'})
# """perform gives back bundle, perform_resources gives back a list of resources"""
# print(search.perform(smart.server).link[0].relation)
# encounters = search.perform_resources(smart.server)
# print(len(encounters))
#
# for e in encounters:
#     print(e.as_json())

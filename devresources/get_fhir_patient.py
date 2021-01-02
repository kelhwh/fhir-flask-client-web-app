from fhirclient import client
from fhirclient.models.fhirsearch import FHIRSearch
from fhirclient.models.encounter import Encounter

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

search = Encounter.where(struct={'patient':patient.id, '_count':'10000'})
encounter = search.perform_resources(smart.server)
print(len(encounter))

"""perform gives back bundle, perform_resources gives back a list of resources"""
search = Encounter.where(struct={'patient':patient.id, '_count':'10000'})
encounters = search.perform_resources(smart.server)
#print(encounters.as_json())

for e in encounters:
    print(e.type[0].text)

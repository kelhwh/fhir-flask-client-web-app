from fhirclient import client

settings = {
    'app_id': 'my_web_app',
    'api_base':  'http://hapi.fhir.org/baseDstu3/'#'https://fhir-open-api-dstu2.smarthealthit.org'
}

smart = client.FHIRClient(settings=settings)

import fhirclient.models.patient as p
patient = p.Patient.read('identifier=http://hl7.org/fhir/sid/us-ssn|999-45-3776', smart.server)

print(patient.birthDate.isostring)

print(smart.human_name(patient.name[0]))


import fhirclient.models.encounter as encounter
#search = p.Procedure.where(struct={'subject': 'hca-pat-1', 'status': 'completed'})
search = encounter.Encounter.where(struct={'subject':'1349276'})
encounters = search.perform_resources(smart.server)
#
# for e in encounters:
#     print(e.as_json())

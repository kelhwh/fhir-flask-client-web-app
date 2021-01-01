from fhirclient.models import domainresource
from application.fhir.connect import smart


class ResourceFinder(domainresource.DomainResource):

    @classmethod
    def find_by_identifier(cls, resource_type: str, identifier_system: str, identifier_value: str, first=False, batch_size=20, page=1):
        cls.resource_type = resource_type
        struct = {
            "identifier": "|".join((identifier_system, identifier_value)),
            "_count": str(batch_size),
            "_offset": str(batch_size*(page-1))
        }
        search = cls.where(struct=struct)

        if first:
            try:
                resource = search.perform_resources(smart.server)[0]
            except:
                resource = None
            return resource
        else:
            resource_list = search.perform_resources(smart.server)
            return resource_list

    @classmethod
    def find_by_patient(cls, resource_type: str, patient: 'patient.Patient', first=False, batch_size=20, page=1):
        cls.resource_type = resource_type
        struct = {
            "patient": patient.id,
            "_count": str(batch_size),
            "_offset": str(batch_size*(page-1))
        }
        search = cls.where(struct=struct)

        if first:
            try:
                resource = search.perform_resources(smart.server)[0]
            except:
                resource = None
            return resource
        else:
            resource_list = search.perform_resources(smart.server)
            return resource_list

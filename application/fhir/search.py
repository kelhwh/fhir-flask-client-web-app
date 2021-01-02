from fhirclient.models import domainresource
from application.fhir.connect import smart


class ResourceFinder(domainresource.DomainResource):
    """
    build() returns a class with desired resource_type, so we can use where
    method to search for the resource we want.

    Batch_size defines the number of resources in a single search result.
    """

    @classmethod
    def build(cls, resource_type: str, batch_size=20) -> 'class':
        cls.resource_type = resource_type
        cls.batch_size = batch_size
        return cls

    @classmethod
    def find_by_identifier(cls, resource_type: str, identifier_system: str, identifier_value: str, first=False, page=1):
        struct = {
            "identifier": "|".join((identifier_system, identifier_value)),
            "_count": str(cls.batch_size),
            "_offset": str(cls.batch_size*(page-1))
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
    def find_by_patient(cls, resource_type: str, patient: 'patient.Patient', first=False, page=1):
        struct = {
            "patient": patient.id,
            "_count": str(cls.batch_size),
            "_offset": str(cls.batch_size*(page-1))
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

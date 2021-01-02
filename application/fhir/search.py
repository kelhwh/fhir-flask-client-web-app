from fhirclient.models import domainresource
from application.fhir.connect import smart


class ResourceFinder(domainresource.DomainResource):

    @classmethod
    def find_by_identifier(cls, resource_type, identifier_system, identifier_value, first=False):
        cls.resource_type = resource_type
        struct = {"identifier": "|".join((identifier_system, identifier_value))}
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

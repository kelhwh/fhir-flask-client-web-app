from fhirclient.models import domainresource, bundle
from application.fhir.connect import smart


class ResourceFinder(domainresource.DomainResource):
    """
    build() returns a class with specified resource_type, so we can use 'where'
    method to search for the given resource.

    Batch_size defines the number of resources in a single search result.
    """


    @classmethod
    def build(cls, resource_type: str, batch_size=20) -> 'class':
        cls.resource_type = resource_type
        cls.batch_size = batch_size
        return cls

    # @classmethod
    # def get(cls, search_parameter=None, first=False, page=1):
    #     struct = {
    #         "_count": str(cls.batch_size),
    #         "_offset": str(cls.batch_size*(page-1))
    #     }
    #     if search_parameter:
    #         struct
    #
    #     search = cls.where(struct=struct)
    #     bundle = search.perform(smart.server)
    #     result = SearchResult(bundle.as_json())
    #
    #     if first:
    #         try:
    #             resource = result.entry[0].resource
    #         except:
    #             resource = None
    #         return resource
    #     else:

    @classmethod
    def get(cls, reference):
        #resource = cls.read(str(id), smart)
        response = smart.server.request_json(reference)
        resource = cls(response)
        return resource

    @classmethod
    def find_by_identifier(cls, identifier_system: str, identifier_value: str, first=False, page=1):
        struct = {
            "identifier": "|".join((identifier_system, identifier_value)),
            "_count": str(cls.batch_size),
            "_offset": str(cls.batch_size*(page-1))
        }
        search = cls.where(struct=struct)
        bundle = search.perform(smart.server)
        result = SearchResult(bundle.as_json())

        if first:
            try:
                resource = result.entry[0].resource
            except:
                resource = None
            return resource
        else:
            return result

    @classmethod
    def find_by_patient(cls, patient_id: str, first=False, page=1):
        struct = {
            "patient": str(patient_id),
            "_count": str(cls.batch_size),
            "_offset": str(cls.batch_size*(page-1))
        }
        search = cls.where(struct=struct)
        bundle = search.perform(smart.server)
        result = SearchResult(bundle.as_json())

        struct.pop("_offset")
        result.total = cls.where(struct=struct).perform(smart.server).total

        if first:
            try:
                resource = result.entry[0].resource
            except:
                resource = None
            return resource
        else:
            return result


class SearchResult(bundle.Bundle):
    """A Bundle resource with some extra methods
    """
    resource_type = "Bundle"

    def __init__(self, jsondict=None, strict=True):
        super(SearchResult, self).__init__(jsondict=jsondict, strict=strict)

    def resource_list(self):
        resources = []
        if self.entry is not None:
            for entry in self.entry:
                resources.append(entry.resource)

        return resources

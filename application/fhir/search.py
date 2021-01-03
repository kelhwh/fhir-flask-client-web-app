from fhirclient.models import domainresource, bundle, fhirsearch
from application.fhir.connect import smart


class ResourceFinder(domainresource.DomainResource):
    """
    build() returns a ResourceFinder object with specified resource_type, so we can use 'where'
    method to search for the given resource.

    Batch_size defines the number of resources in a single search result.
    """
    #resource_type = "ResourceFinder"

    def __init__(self, resource_type, batch_size, jsondict=None, strict=True):
        self.resource_type = resource_type
        self.batch_size = batch_size


    @classmethod
    def build(cls, resource_type: str, batch_size=20):
        return cls(resource_type, batch_size)


    def get(self, search_params=None, first=False, page=1, debug=False):
        struct = {
            "_count": str(self.batch_size),
            "_offset": str(self.batch_size*(page-1))
        }
        if search_params:
            for key, val in search_params.items():
                struct[key] = val

        search = fhirsearch.FHIRSearch(self, struct)
        if debug:
            print("{} has resource type '{}', search criteria: {} ".format(self.__class__, self.resource_type, search.construct()))

        bundle = search.perform(smart.server)
        result = SearchResult(bundle.as_json())

        struct.pop("_offset")
        result.total = fhirsearch.FHIRSearch(self, struct).perform(smart.server).total

        if first:
            try:
                resource = result.entry[0].resource
            except:
                resource = None
            return resource
        else:
            return result


    def find_by_identifier(self, identifier_system: str, identifier_value: str, **kwargs):
        search_params = {"identifier": "|".join((identifier_system, identifier_value))}
        return self.get(search_params=search_params, **kwargs)


    def find_by_patient(self, patient_id: str, **kwargs):
        search_params = {"patient": str(patient_id)}
        return self.get(search_params=search_params, **kwargs)


    def find_by_id(self, id: str, **kwargs):
        search_params = {"_id": str(id)}
        return self.get(search_params=search_params, first=True, page=1, **kwargs)


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

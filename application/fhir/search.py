from fhirclient.models import domainresource, bundle, fhirsearch
from application.fhir.connect import smart


class ResourceFinder(domainresource.DomainResource):
    """
    build() returns a ResourceFinder object with specified resource_type, so we can use 'where'
    method to search for the given resource.

    Batch_size defines the number of resources in a single search result.
    """

    def __init__(self, resource_type, jsondict=None, strict=True):
        self.resource_type = resource_type


    @classmethod
    def build(cls, resource_type: str):
        """ Returns a ResourceFinder object with specified resource tpye.
        """
        return cls(resource_type)


    def get(self, search_params=None, first=False, batch_size=20, page=1, debug=False):
        """ Perform search for specific resource.

        search_params dict: searh parameters other than _count and _offset in dictionary
        first bool: returns one resource or a list of resrouces
        batch_size int: number of resources in the list
        page int: number of page of the result if there are more than one page
        """
        struct = {
            "_count": str(batch_size),
            "_offset": str(batch_size*(page-1))
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
        """ Perform resource search by identifier, built on top of self.get()
        """
        search_params = {"identifier": "|".join((identifier_system, identifier_value))}
        return self.get(search_params=search_params, **kwargs)


    def find_by_patient(self, patient_id: str, **kwargs):
        """ Perform resource search by patient_id, built on top of self.get()
        """
        search_params = {"patient": str(patient_id)}
        return self.get(search_params=search_params, **kwargs)


    def find_by_id(self, id: str, **kwargs):
        """ Perform resource search by resource id, built on top of self.get()
        """
        search_params = {"_id": str(id)}
        return self.get(search_params=search_params, first=True, page=1, **kwargs)


class SearchResult(bundle.Bundle):
    """A Bundle resource with extra methods.
    """
    resource_type = "Bundle"

    def __init__(self, jsondict=None, strict=True):
        super(SearchResult, self).__init__(jsondict=jsondict, strict=strict)

    def resource_list(self):
        """ Returns a list of resources.
        """
        resources = []
        if self.entry is not None:
            for entry in self.entry:
                resources.append(entry.resource)

        return resources

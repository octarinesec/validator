import octactl
from config import Config
from violations.violations_list import ViolationsList
from violations.violations_summary import ViolationsSummary
from violations.attribute_filter import AttributeFilter


class Violations():
    """ A class set to process violations on variety of display options (e.g summary,list) """
    def process(*args, **kwargs):
        return Violations(*args, **kwargs)._run()

    def __init__(self):
        self.attribute_filter = AttributeFilter()
        self.summary = ViolationsSummary(self.attribute_filter)
        self.violations_list = ViolationsList(self.attribute_filter)
        self.include_namesapace = False
        self.empty = True

    @property
    def displayable(self) -> List(Displayable):
        """ Displayable retrun an array of objects to meet the "Displayable interface" """
        return [self.summary, self.violations_list]

    def _run(self):
        js = octactl.run_octactl()
        if len(js['violated_resources']) > 0:
            for resource in js['violated_resources']:
                ns = self._namespace(resource)
                violation = resource['violations']
                key = resource['resource_kind'] + ":" + resource['resource_name'] + ":" + ns
                metadata = {'Name': resource['resource_name'], 'Kind': resource['resource_kind'], 'Namespace': ns, "Filename": resource['file_path']}
                self.summary.set(violation, metadata, key)
                self.violations_list.set(violation, metadata, key)
            self.empty = False
        self._whitelist_unused_attributes()
        if len(js['errors']):
            self.errors = js['errors']
        return self

    def _namespace(self, resource):
        if "namespace" in resource:
            self.include_namesapace = True
            return resource['namespace']
        return 'None'

    def _whitelist_unused_attributes(self):
        if (not self.include_namesapace) and (not Config.always_display_namespace):
            self.attribute_filter.exclude_attributes = "Namespace"
        if Config.helm:
            self.attribute_filter.exclude_attributes = "Filename"

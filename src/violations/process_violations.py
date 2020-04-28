import set_config as config
import octactl
from violations.violations_list import ViolationsList
from violations.violations_summary import ViolationsSummary
from violations.attribute_filter import AttributeFilter


class ProcessViolations():
    def __init__(self):
        self.attribute_filter = AttributeFilter()
        self.summary = ViolationsSummary(self.attribute_filter)
        self.violations_list = ViolationsList(self.attribute_filter)
        self.include_namesapace = False

    def run(self):
        js = octactl.run_octactl()
        if len(js['violated_resources']) > 0:
            for resource in js['violated_resources']:
                violation = resource['violations']
                key = resource['resource_kind'] + ":" + resource['resource_name']
                metadata = {'Name': resource['resource_name'], 'Kind': resource['resource_kind'], 'Namespace': self._namespace(resource), "Filename": resource['file_path']}
                self.summary.set(violation, metadata, key)
                self.violations_list.set(violation, metadata, key)
        self._whitelist_unused_attributes()
        return self

    def _namespace(self, resource):
        if "namespace" in resource:
            self.include_namesapace = True
            return resource['namespace']
        return 'None'

    def _whitelist_unused_headers(self):
        if (not self.include_namesapace) and (not config.always_display_namespace()):
            self.attribute_filter.exclude_attributes = "Namespace"
        if config.helm():
            self.attribute_filter.exclude_attributes = "Filename"

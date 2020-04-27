import set_config as config
import octactl
from violations.violations_list import ViolationsList
from violations.violations_summary import ViolationsSummary


class ProcessViolations():
    def __init__(self):
        self.summary = ViolationsSummary()
        self.violations_list = ViolationsList()
        self.namespace_not_none = False

    def run(self):
        js = octactl.run_octactl()
        if len(js['violated_resources']) > 0:
            for resource in js['violated_resources']:
                violation = resource['violations']
                key = resource['resource_kind'] + ":" + resource['resource_name']
                metadata = {'Name': resource['resource_name'], 'Kind': resource['resource_kind'], 'Namespace': self._namespace(resource), "Filename": resource['file_path']}
                self.summary.set(violation, metadata, key)
                self.violations_list.set(violation, metadata, key)
        self._whitelist_unused_headers()
        return self

    def _namespace(self, resource):
        if "namespace" in resource:
            self.namespace_not_none = True
            return resource['namespace']
        return 'None'

    def _whitelist_unused_headers(self):
        if (not self.namespace_not_none) and (not config.always_display_namespace()):
            self.violations_list.exclude_fields = "Namespace"
            self.summary.exclude_fields = "Namespace"
        if config.helm():
            self.violations_list.exclude_fields = "Filename"
            self.summary.exclude_fields = "Filename"

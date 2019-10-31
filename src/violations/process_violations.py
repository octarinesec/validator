from cmd_run.octactl import Octactl
from violations.violations_list import ViolationsList
from violations.violations_summary import ViolationsSummary


class ProcessViolations():
    def __init__(self, config):
        self.config = config
        self.summary = ViolationsSummary()
        self.violations_list = ViolationsList()

    def run(self):
        js = Octactl(self.config).run()
        if len(js['violated_resources']) > 0:
            for resource in js['violated_resources']:
                violation = resource['violations']
                key = resource['resource_kind'] + ":" + resource['resource_name']
                metadata = {'Name': resource['resource_kind'], 'Kind': resource['resource_name']}
                self.summary.set(violation, metadata, key)
                self.violations_list.set(violation, metadata, key)
        return self

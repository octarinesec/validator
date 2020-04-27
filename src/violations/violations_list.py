
from tabulate import tabulate
from violations.violations import Violations


class ViolationsList(Violations):
    VIOLATION_MAP = {
        "Violation Name": 'violation_name',
        "Violation Category": 'violation_category',
        "Violation Description": 'description'
    }

    """
    VIOLATION_MAP is set to help dynamically map the validator table header(the key) to the octactl result field(the value)
    This can help us easily change the map in case our api result changes
    For example octactl result of :
        {
          "description": "Privileged container: hello-octarine (CIS 1.7.1)",
          "violation_type": "privileged-container",
        }
    will resolve to
        {
          "Violation Type": "privileged-container",
          "Violation Category": "SecurityContext"
         }

    """

    def __init__(self):
        self.violations = {}
        self._exclude_fields = []

    def set(self, violations, metadata, key):
        # Define the violation metadata from VIOLATION_MAP constant"
        def violation_metadata_from_dict(v):
            return {k: v[self.VIOLATION_MAP[k]] for k, _ in self.VIOLATION_MAP.items()}

        # Create an array of violations with the needed metadata
        lst = map(violation_metadata_from_dict, violations)
        self.violations[key] = {**metadata, 'violations': list(lst)}

    def get(self):
        return self.violations

    def pritify(self):
        # Make a copy of violations so it can be mutated
        violations_for_display = self.violations
        violations_list = [self._setHeaders()]
        for uniq_key in violations_for_display.keys():
            # Remove the excluded fields
            for exc in self._exclude_fields:
                violations_for_display[uniq_key].pop(exc)
            key_violations = violations_for_display[uniq_key].pop('violations')
            for i in key_violations:
                violations_list.append(list(violations_for_display[uniq_key].values()) + list(i.values()))
        return (tabulate(violations_list, headers="firstrow", tablefmt="orgtbl"))

    def _setHeaders(self):
        "Dynamically extract the header,The expected object structure is {'k':'v',...k:['k','v'...]}"
        "Use the keys of the first result as a header"
        first_uniq_key = self.violations[list(self.violations)[0]]
        # Find the violation key - where the value is an array
        array_key = list({k: v for k, v in first_uniq_key.items() if type(v) == list})[0]
        # Exclude the array_key and the excluded headers from the array
        main_object_keys = [x for x in list(first_uniq_key) if (x not in self._exclude_fields) and (x != array_key)]
        return main_object_keys + list(first_uniq_key[array_key][0])


from tabulate import tabulate


class ViolationsList:
    VIOLATION_MAP = {
        "Violation Type": 'violation_type',
        "Violation Category": 'description'
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

    def set(self, violations, metadata, key):
        "Define the violation metadata from VIOLATION_MAP constant"
        def violation_metadata_from_dict(v):
            return {k: v[self.VIOLATION_MAP[k]] for k, _ in self.VIOLATION_MAP.items()}

        "Create an array of violations with the needed metadata"
        lst = map(violation_metadata_from_dict, violations)
        self.violations[key] = {**metadata, 'violations': list(lst)}

    def get(self):
        return self.violations

    def pritify(self):
        violations_list = [self._setHeaders()]
        for uniq_key in self.violations.keys():
            key_violations = self.violations[uniq_key].pop('violations')
            for i in key_violations:
                violations_list.append(list(self.violations[uniq_key].values()) + list(i.values()))
        return (tabulate(violations_list, headers="firstrow", tablefmt="orgtbl"))

    def _setHeaders(self):
        "Dynamically extract the header,The expected object structure is {'k':'v',...k:['k','v'...]}"
        "Use the keys of the first result as a header"
        first_uniq_key = self.violations[list(self.violations)[0]]
        "Find the key where the value is an array"
        array_key = list({k: v for k, v in first_uniq_key.items() if type(v) == list})[0]
        main_object_keys = [x for x in list(first_uniq_key) if x != array_key]
        return main_object_keys + list(first_uniq_key[array_key][0])

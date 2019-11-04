from tabulate import tabulate


class ViolationsSummary:
    def __init__(self):
        self.summary = {}

    def set(self, violations, metadata, key):
        self.summary[key] = {**metadata, 'Number': len(violations)}

    def get(self):
        return self.summary

    def pritify(self):
        " Use the keys of the first result as a header "
        violations_uniq_keys = list(self.summary)
        sum = [list(self.summary[violations_uniq_keys[0]])]
        " Iterate through the dict values to print the results "
        for k in violations_uniq_keys:
            sum.append(self.summary[k].values())
        return (tabulate(sum, headers="firstrow", tablefmt="orgtbl"))

from tabulate import tabulate


class ViolationsSummary():
    def __init__(self, f):
        self.summary = {}
        self.filter = f

    def set(self, violations, metadata, key):
        self.summary[key] = {**metadata, 'Violations': len(violations)}

    def get(self):
        return self.summary

    def pritify(self):
        """
        Print the result in a table
        """
        # Use the keys of the first result as a header
        violations_uniq_keys = list(self.summary)
        sum = [[x for x in list(self.summary[violations_uniq_keys[0]]) if (x not in self.filter.exclude_attributes)]]
        # Iterate through the dict values to print the results
        for k in violations_uniq_keys:
            # Make a copy of violations so it can be mutated
            summary_for_display = self.summary[k]
            for exc in self.filter.exclude_attributes:
                summary_for_display.pop(exc)
            sum.append(summary_for_display.values())
        return (tabulate(sum, headers="firstrow", tablefmt="orgtbl"))

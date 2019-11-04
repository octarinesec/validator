#!/usr/bin/python3

from violations.process_violations import ProcessViolations
import set_config as config
from print_result import print_results
import json


if __name__ == "__main__":
    config.validate_config()
    violations = ProcessViolations().run()
    if len(violations.summary.get()) > 0:
        if config.output_file():
            if len(violations.summary.get()):
                with open(config.output_file(), 'w') as fd:
                    json.dump(violations.violations_list.get(), fd, indent=4, separators=(',', ': '), sort_keys=True)
        else:
            print(print_results(config, violations))
        config.exitWithError()

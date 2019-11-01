#!/usr/bin/python3

from violations.process_violations import ProcessViolations
from set_config import SetConfig
from print_result import print_results
import json


if __name__ == "__main__":
    " Set the config based on the Environment variable provided at runtime "
    config = SetConfig()
    violations = ProcessViolations(config).run()
    if config.output_file():
        if len(violations.summary.get()):
            with open(config.output_file(), 'w') as fd:
                json.dump(violations.violations_list.get(), fd, indent=4, separators=(',', ': '), sort_keys=True)
    else:
        print(print_results(config, violations))

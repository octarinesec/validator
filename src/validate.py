#!/usr/bin/python3

from violations.process_violations import ProcessViolations
from config import Config
from print_result import print_results
import json


if __name__ == "__main__":
    Config.validate_config()
    violations = ProcessViolations().run()
    if len(violations.summary.get()) > 0:
        if Config.output_file:
            if len(violations.summary.get()):
                with open(Config.output_file, 'w') as fd:
                    json.dump(violations.violations_list.get(), fd, indent=4, separators=(',', ': '), sort_keys=True)
        else:
            print(print_results(violations))
    else:
        print("No violations has been detected!")

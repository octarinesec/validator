#!/usr/bin/python3

from violations.process_violations import ProcessViolations
from set_config import SetConfig
from print_result import print_results


if __name__ == "__main__":
    "Set the config based on the Environment variable provided at runtime "
    config = SetConfig()
    violations = ProcessViolations(config).run()
    print(print_results(config, violations))

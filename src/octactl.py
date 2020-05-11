import json
from config import Config
from plumbum.cmd import octactl, helm
from plumbum.commands.processes import ProcessExecutionError

GUARDRAIL = octactl['guardrail']['validate']['policy']


def run_octactl():
    if Config.helm:
        return _run_with_helm()
    else:
        return _run_with_file_or_directory()


def _run_with_file_or_directory():
    return _run_octactl_command(Config.file_objects)


def _run_octactl_command(file_or_directory):
    try:
        result = GUARDRAIL.run(['-f', file_or_directory])
    except ProcessExecutionError as err:
        print("Fail to run the validate command! {}".format(err))
        Config.exitWithError()
    return json.loads(result[1])


def _run_with_helm():
    tmp_file_location = "/tmp/validator_tmp_file.yaml"
    try:
        (helm["template"][Config.helm.split(" ")] > tmp_file_location)()
    except ProcessExecutionError as err:
        print("Fail to run helm with {} parameters. error: {}".format(helm(), err))
    return _run_octactl_command(tmp_file_location)

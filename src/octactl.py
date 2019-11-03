import json
import set_config as config
from plumbum.cmd import octactl, helm
from plumbum.commands.processes import ProcessExecutionError

GUARDRAIL = octactl['guardrail']['validate']['policy']


def run_octactl():

    if config.helm():
        return _run_with_helm()
    else:
        return _run_with_file_or_direcoty()


def _run_with_file_or_direcoty():
    try:
        result = GUARDRAIL.run(['-f', config.file_objects()])
    except ProcessExecutionError as err:
        print("Fail to run the validate command! {}".format(err))
        config.exitWithError()
    return json.loads(result[1])


def _run_with_helm():
    " TODO: test and complete helm"
    chain = helm(config.helm()).split(" ") | GUARDRAIL.run(['-f', '-'])
    try:
        result = chain.run()
    except ProcessExecutionError as err:
        print("Fail to run the validate command! {}".format(err))
    return json.loads(result[1])

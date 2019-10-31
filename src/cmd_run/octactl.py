import json
from plumbum.cmd import octactl, helm
from plumbum.commands.processes import ProcessExecutionError


class Octactl():
    def __init__(self, config):
        self.config = config
        self.guardrail = octactl['guardrail']['validate']['policy']

    def run(self):
        if self.config.helm():
            return self._run_with_helm()
        else:
            return self._run_with_file_or_direcoty()

    def _run_with_file_or_direcoty(self):
        try:
            result = self.guardrail.run(['-f', self.config.file_objects()])
        except ProcessExecutionError as err:
            print("Fail to run the validate command! {}".format(err))
            self.config.exitWithError()
        return json.loads(result[1])

    def _run_with_helm(self):
        chain = helm(self.config.helm()).split(" ") | self.guardrail.run(['-f', '-'])
        try:
            result = chain.run()
        except ProcessExecutionError as err:
            print("Fail to run the validate command! {}".format(err))
        return json.loads(result[1])

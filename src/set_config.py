import os


class SetConfig:
    def __init__(self):
        self.validate_config()

    def validate_config(self):
        ENV_TO_CHECK = ["OCTARINE_ACCOUNT",
                        "OCTARINE_SESSION_ID", "OCTARINE_SESSION_ACCESSJWT", "OBJECT_DIR"]
        if not all(elem in os.environ for elem in ENV_TO_CHECK):
            print("Missing one or more config variable, please make sure {} is set".format(
                ','.join(ENV_TO_CHECK)))
            raise SystemExit

    def namespace(self):
        if os.environ.get("NAMESPACE"):
            return os.environ.get("NAMESPACE")
        else:
            return "default"

    def output_file(self):
        if "OUTPUT_FILE_PATH" in os.environ:
            return os.environ.get("OUTPUT_FILE_PATH")

    def domain(self):
        # TODO add logic to pull the first domain if DOMAIN env var does not exists
        return os.environ.get("DOMAIN")

    def file_objects(self):
        return os.environ.get("OBJECT_DIR")

    def exitWithNoErrors(self):
        exit(0)

    def exitWithError(self):
        exit(1)

    def helm(self):
        if os.environ.get("HELM_COMMAND"):
            return os.environ.get("HELM_COMMAND")
        else:
            return None

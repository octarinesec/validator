import os


def validate_config():
    ENV_TO_CHECK = ["OCTARINE_ACCOUNT",
                    "OCTARINE_SESSION_ID", "OCTARINE_SESSION_ACCESSJWT", "OBJECT_DIR"]

    if not set(ENV_TO_CHECK).issubset(os.environ):
        print("Missing one or more config variable, please make sure {} is set".format(
            ','.join(ENV_TO_CHECK)))
        raise SystemExit
    return True


def namespace():
    if os.getenv("NAMESPACE"):
        return os.getenv("NAMESPACE")
    else:
        return "default"


def output_file():
    return os.getenv("OUTPUT_FILE_PATH")


def domain():
    # TODO add logic to pull the first domain if DOMAIN env var does not exists
    return os.getenv("DOMAIN")


def file_objects():
    return os.getenv("OBJECT_DIR")


def exitWithNoErrors():
    exit(0)


def exitWithError():
    exit(1)


def helm():
    return os.getenv("HELM_COMMAND")

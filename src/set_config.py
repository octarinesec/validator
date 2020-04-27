import os


def validate_config():
    ENV_TO_CHECK = ["OCTARINE_ACCOUNT",
                    "OCTARINE_SESSION_ID", "OCTARINE_SESSION_ACCESSJWT"]

    if not set(ENV_TO_CHECK).issubset(os.environ):
        print("Missing one or more Octarine config variable, please make sure {} is set".format(
            ','.join(ENV_TO_CHECK)))
        raise SystemExit
    if (not os.getenv("OBJECT_DIR")) and (not os.getenv("HELM_COMMAND")):
        print("Missing file input to validate, please make sure either FILE_OBJECT or HELM_COMMAND is set")
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
    if not os.path.exists(os.getenv("OBJECT_DIR")):
        print("Cannot find file or diretory at {}".format(os.getenv("OBJECT_DIR")))
        raise SystemExit
    return os.getenv("OBJECT_DIR")


def always_display_namespace():
    if os.getenv("ALWAYS_DISPLAY_NAMESPACE"):
        return os.getenv("ALWAYS_DISPLAY_NAMESPACE")
    else:
        return False


def exitWithNoErrors():
    exit(0)


def exitWithError():
    exit(1)


def helm():
    return os.getenv("HELM_COMMAND")

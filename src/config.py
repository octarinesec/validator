import os


class ConfigError(Exception):
    pass


class MetaConfig(type):
    """  This Metaclass sets all configs as attributes for the Config class by using decriptors """
    @property
    def helm(cls):
        return os.getenv("HELM_COMMAND")

    @property
    def policy_name(cls):
        return os.getenv("POLICY_NAME")

    @property
    def always_display_namespace(cls):
        return bool(os.getenv("ALWAYS_DISPLAY_NAMESPACE")) or False

    @property
    def file_objects(cls):
        try:
            if not os.path.exists(os.getenv("OBJECT_DIR")):
                print("Cannot find file or diretory at {}".format(os.getenv("OBJECT_DIR")))
                raise SystemExit
        except TypeError as e:
            print("Missing file input to validate, please make sure either OBJECT_DIR exists")
            exit(1)
        return os.getenv("OBJECT_DIR")

    @property
    def namespace(cls):
        return os.getenv("NAMESPACE") or "default"

    @property
    def output_file(cls):
        return os.getenv("OUTPUT_FILE_PATH")

    @property
    def domain(cls):
        return os.getenv("DOMAIN")

    def __getattr__(cls, name):
        if (os.getenv(name.upper())):
            return os.getenv(name.upper())
        else:
            raise ConfigError("Cannot find config {}".format(name))


class Config(metaclass=MetaConfig):
    def exitWithNoErrors():
        exit(0)

    def exitWithError():
        exit(1)

    def validate_config():
        ENV_TO_CHECK = ["OCTARINE_ACCOUNT",
                        "OCTARINE_SESSION_ID", "OCTARINE_SESSION_ACCESSJWT"]

        if not set(ENV_TO_CHECK).issubset(os.environ):
            print("Missing one or more Octarine config variable, please make sure {} is set".format(
                ','.join(ENV_TO_CHECK)))
            raise SystemExit
        if (not os.getenv("OBJECT_DIR")) and (not os.getenv("HELM_COMMAND")):
            print("Missing file input to validate, please make sure either OBJECT_DIR or HELM_COMMAND is set")
            raise SystemExit

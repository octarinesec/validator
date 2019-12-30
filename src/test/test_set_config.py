import pytest
import os
import set_config as config


def test_validate_config_with_missing_params():
    if "OCTARINE_ACCOUNT" in os.environ.keys():
        del os.environ['OCTARINE_ACCOUNT']
    with pytest.raises(SystemExit):
        config.validate_config()


def test_validate_config_with_env_var():
    os.environ['OCTARINE_ACCOUNT'] = "some_account"
    os.environ['OCTARINE_SESSION_ID'] = "some_session_id"
    os.environ['OCTARINE_SESSION_ACCESSJWT'] = "some_session_access_jwt"
    os.environ['OBJECT_DIR'] = "some_file"
    assert config.validate_config() == True


def test_namespace_with_env_var_set():
    ns_value = "test"
    os.environ['NAMESPACE'] = ns_value
    assert config.namespace() == ns_value


def test_namespace_with_no_env_var_set():
    if "NAMESPACE" in os.environ.keys():
        del os.environ['NAMESPACE']
    assert config.namespace() == "default"


def test_domain():
    domain = "domain"
    os.environ["DOMAIN"] = domain
    assert config.domain() == domain


def test_none_exists_file_or_directory_file_objects():
    os.environ["OBJECT_DIR"] = "none_exists_dir"
    with pytest.raises(SystemExit):
        config.file_objects()


def test_with_existing_file_file_objects():
    os.environ["OBJECT_DIR"] = "src/test/test_set_config.py"
    assert config.file_objects() == "src/test/test_set_config.py"


def test_with_existing_directory_file_objects():
    os.environ["OBJECT_DIR"] = "src/test"
    assert config.file_objects() == "src/test"

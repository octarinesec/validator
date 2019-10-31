import pytest
import os
from set_config import SetConfig


def test_validate_config_with_missing_params():
    if "OCTARINE_ACCOUNT" in os.environ.keys():
        del os.environ['OCTARINE_ACCOUNT']
    with pytest.raises(SystemExit):
        cfg = SetConfig()


def test_validate_config_with_env_var():
    os.environ['OCTARINE_ACCOUNT'] = "some_account"
    os.environ['OCTARINE_SESSION_ID'] = "some_session_id"
    os.environ['OCTARINE_SESSION_ACCESSJWT'] = "some_session_access_jwt"
    os.environ['OBJECT_FILE'] = "some_file"
    cfg = SetConfig()
    assert isinstance(cfg, SetConfig)


def test_namespace_with_env_var_set():
    ns_value = "test"
    os.environ['NAMESPACE'] = ns_value
    cfg = SetConfig()
    assert cfg.namespace() == ns_value


def test_namespace_with_no_env_var_set():
    if "NAMESPACE" in os.environ.keys():
        del os.environ['NAMESPACE']
    cfg = SetConfig()
    assert cfg.namespace() == "default"


def test_domain():
    domain = "domain"
    os.environ["DOMAIN"] = domain
    cfg = SetConfig()
    assert cfg.domain() == domain

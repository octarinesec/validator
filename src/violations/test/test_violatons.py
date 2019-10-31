import pytest
from violations.violations_summary import ViolationsSummary
from violations.violations_list import ViolationsList

""" Helper functions ot be used by all tests """


def _metadata():
    return {'key': 'value'}


def _violations():
    return [
        {
            "description": "Privileged container: hello-octarine (CIS 1.7.1)",
            "violation_type": "privileged-container"
        },
        {
            "description": "Share host network container: hello-octarine (CIS 1.7.4)",
            "violation_type": "share-host-network-container"
        },
        {
            "description": "container hello-octarine capability added: CAP_SYS_ADMIN",
            "violation_type": "container-sys-admin-cap-added"
        }
    ]


def _key():
    return "Kind:Name"


def _keys():
    return ["Kind{}:Name{}".format(x, x) for x in range(5)]


@pytest.fixture
def new_summary_instance():
    summary = ViolationsSummary()
    summary.set(_violations(), _metadata(), _key())
    return summary


@pytest.fixture
def new_violations_instance():
    violations = ViolationsList()
    violations.set(_violations(), _metadata(), _key())
    return violations


""" Test ViolationsSummary """


def test_init_summary(new_summary_instance):
    assert isinstance(new_summary_instance, ViolationsSummary)
    assert type(new_summary_instance.summary) == dict


def test_set_for_single_key(new_summary_instance):
    assert new_summary_instance.summary[_key()] == {**_metadata(), 'Number': 3}


def test_set_for_many_keys(new_summary_instance):
    for key in _keys():
        new_summary_instance.set(_violations(), _metadata(), key)
    assert len(new_summary_instance.summary.keys()) == len(_keys())+1


def test_get(new_summary_instance):
    assert new_summary_instance.get() == {_key(): {**_metadata(), 'Number': 2}}


def test_prtify_output_for_single_key(new_summary_instance):
    "Output: plain with headers"
    expected = "\n".join(['| key   |   Number |', '|-------+----------|', '| value |        2 |', ])
    assert new_summary_instance.pritify() == expected


""" Test ViolationsList """


def test_init_violations_list(new_violations_instance):
    assert isinstance(new_violations_instance, ViolationsList)
    assert type(new_violations_instance.violations) == dict


def test_set_for_single_key(new_violations_instance):
    vio = new_violations_instance.violations[_key()]['violations']
    assert len(vio) == 3
    assert vio[0] == {'Violation Category': 'Privileged container: hello-octarine (CIS 1.7.1)', 'Violation Type': 'privileged-container'}


def test_set_for_many_keys(new_violations_instance):
    for key in _keys():
        new_violations_instance.set(_violations(), _metadata(), key)
    assert len(new_violations_instance.violations.keys()) == len(_keys())+1


def test_get(new_violations_instance):
    assert list(new_violations_instance.get().keys()) == [_key()]
    assert list(new_violations_instance.get()[_key()].keys()) == list(_metadata().keys()) + ['violations']
    assert len(new_violations_instance.get()[_key()]['violations']) == 3
    assert new_violations_instance.get()[_key()]['violations'][0] == {'Violation Category': 'Privileged container: hello-octarine (CIS 1.7.1)', 'Violation Type': 'privileged-container'}


def test_prtify_output_for_single_key(new_violations_instance):
    expected = "\n".join(['| key   | Violation Type                | Violation Category                                       |',
                          '|-------+-------------------------------+----------------------------------------------------------|',
                          '| value | privileged-container          | Privileged container: hello-octarine (CIS 1.7.1)         |',
                          '| value | share-host-network-container  | Share host network container: hello-octarine (CIS 1.7.4) |',
                          '| value | container-sys-admin-cap-added | container hello-octarine capability added: CAP_SYS_ADMIN |'])

    assert new_violations_instance.pritify() == expected

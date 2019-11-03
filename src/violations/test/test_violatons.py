import pytest
from violations.violations_summary import ViolationsSummary
from violations.violations_list import ViolationsList
import violations.test.data.data_helper as data


@pytest.fixture
def new_summary_instance():
    summary = ViolationsSummary()
    summary.set(data.violations(), data.metadata(), data.key())
    return summary


@pytest.fixture
def new_violations_instance():
    violations = ViolationsList()
    violations.set(data.violations(), data.metadata(), data.key())
    return violations


class TestViolationSummary():
    """ Test ViolationsSummary """

    def test_init_summary(self, new_summary_instance):
        assert isinstance(new_summary_instance, ViolationsSummary)
        assert type(new_summary_instance.summary) == dict

    def test_set_for_single_key(self, new_summary_instance):
        assert new_summary_instance.summary[data.key()] == {**data.metadata(), 'Number': 3}

    def test_set_for_many_keys(self, new_summary_instance):
        for key in data.keys():
            new_summary_instance.set(data.violations(), data.metadata(), key)
        assert len(new_summary_instance.summary.keys()) == len(data.keys())+1

    def test_get(self, new_summary_instance):
        assert new_summary_instance.get() == {data.key(): {**data.metadata(), 'Number': 3}}

    def test_prtify_output_for_single_key(self, new_summary_instance):
        "Output: plain with headers"
        expected = "\n".join(['| key   |   Number |', '|-------+----------|', '| value |        3 |', ])
        assert new_summary_instance.pritify() == expected


class TestViolationList():
    " Test ViolationsList "

    def test_init_violations_list(self, new_violations_instance):
        assert isinstance(new_violations_instance, ViolationsList)
        assert type(new_violations_instance.violations) == dict

    def test_set_for_single_key(self, new_violations_instance):
        vio = new_violations_instance.violations[data.key()]['violations']
        assert len(vio) == 3
        assert vio[0] == {'Violation Category': 'Privileged container: hello-octarine (CIS 1.7.1)', 'Violation Type': 'privileged-container'}

    def test_set_for_many_keys(self, new_violations_instance):
        for key in data.keys():
            new_violations_instance.set(data.violations(), data.metadata(), key)
        assert len(new_violations_instance.violations.keys()) == len(data.keys())+1

    def test_get(self, new_violations_instance):
        assert list(new_violations_instance.get().keys()) == [data.key()]
        assert list(new_violations_instance.get()[data.key()].keys()) == list(data.metadata().keys()) + ['violations']
        assert len(new_violations_instance.get()[data.key()]['violations']) == 3
        assert new_violations_instance.get()[data.key()]['violations'][0] == {'Violation Category': 'Privileged container: hello-octarine (CIS 1.7.1)', 'Violation Type': 'privileged-container'}

    def test_prtify_output_for_single_key(self, new_violations_instance):
        expected = "\n".join(['| key   | Violation Type                | Violation Category                                       |',
                              '|-------+-------------------------------+----------------------------------------------------------|',
                              '| value | privileged-container          | Privileged container: hello-octarine (CIS 1.7.1)         |',
                              '| value | share-host-network-container  | Share host network container: hello-octarine (CIS 1.7.4) |',
                              '| value | container-sys-admin-cap-added | container hello-octarine capability added: CAP_SYS_ADMIN |'])

        assert new_violations_instance.pritify() == expected

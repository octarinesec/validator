import pytest
from violations.violations_summary import ViolationsSummary
from violations.violations_list import ViolationsList
from violations.attribute_filter import AttributeFilter
import violations.test.data.data_helper as data


@pytest.fixture
def new_summary_instance():
    f = AttributeFilter()
    summary = ViolationsSummary(f)
    summary.set(data.violations(), data.metadata(), data.key())
    return summary


@pytest.fixture
def new_violations_instance():
    f = AttributeFilter()
    violations = ViolationsList(f)
    violations.set(data.violations(), data.metadata(), data.key())
    return violations


class TestViolationSummary():
    """ Test ViolationsSummary """

    def test_init_summary(self, new_summary_instance):
        assert isinstance(new_summary_instance, ViolationsSummary)
        assert type(new_summary_instance.summary) == dict

    def test_set_for_single_key(self, new_summary_instance):
        assert new_summary_instance.summary[data.key()] == {**data.metadata(), 'Violations': 3}

    def test_set_for_many_keys(self, new_summary_instance):
        for key in data.keys():
            new_summary_instance.set(data.violations(), data.metadata(), key)
        assert len(new_summary_instance.summary.keys()) == len(data.keys())+1

    def test_get(self, new_summary_instance):
        assert new_summary_instance.get() == {data.key(): {**data.metadata(), 'Violations': 3}}

    def test_prtify_output_for_single_key(self, new_summary_instance):
        "Output: plain with headers"
        expected = "\n".join(['| key   |   Violations |', '|-------+--------------|', '| value |            3 |', ])
        assert new_summary_instance.pritify() == expected

    def test_filtered_output_for_single_key(self):
        f = AttributeFilter()
        summary = ViolationsSummary(f)
        summary.set(data.violations(), data.metadata_with_filtered_data(), data.key())
        f.exclude_attributes = "key1"
        assert summary.get() == {'Kind:Name': {'key': 'value', 'key1': 'value1', 'key2': 'value2', 'Violations': 3}}
        expected = "\n".join(['| key   | key2   |   Violations |', '|-------+--------+--------------|', '| value | value2 |            3 |', ])
        assert summary.pritify() == expected


class TestViolationList():
    " Test ViolationsList "

    def test_init_violations_list(self, new_violations_instance):
        assert isinstance(new_violations_instance, ViolationsList)
        assert type(new_violations_instance.violations) == dict

    def test_set_for_single_key(self, new_violations_instance):
        vio = new_violations_instance.violations[data.key()]['violations']
        assert len(vio) == 3
        assert vio[0] == {'Violation Name': 'privileged-container', 'Violation Category': 'SecurityContext'}

    def test_set_for_many_keys(self, new_violations_instance):
        for key in data.keys():
            new_violations_instance.set(data.violations(), data.metadata(), key)
        assert len(new_violations_instance.violations.keys()) == len(data.keys())+1

    def test_get(self, new_violations_instance):
        assert list(new_violations_instance.get().keys()) == [data.key()]
        assert list(new_violations_instance.get()[data.key()].keys()) == list(data.metadata().keys()) + ['violations']
        assert len(new_violations_instance.get()[data.key()]['violations']) == 3
        assert new_violations_instance.get()[data.key()]['violations'][0] == {
            'Violation Name': 'privileged-container', 'Violation Category': 'SecurityContext'}

    def test_prtify_output_for_single_key(self, new_violations_instance):
        expected = "\n".join(['| key   | Violation Name                | Violation Category   |',
                              '|-------+-------------------------------+----------------------|',
                              '| value | privileged-container          | SecurityContext      |',
                              '| value | share-host-network-container  | SecurityContext      |',
                              '| value | container-sys-admin-cap-added | SecurityContext      |'])
        assert new_violations_instance.pritify() == expected

    def test_filtered_output_for_single_key(self):
        f = AttributeFilter()
        lst = ViolationsList(f)
        violations = ViolationsList(f)
        violations.set(data.violations(), data.metadata_with_filtered_data(), data.key())
        f.exclude_attributes = "key1"
        assert violations.get() == {'Kind:Name': {'key': 'value', 'key1': 'value1', 'key2': 'value2', 'violations': [{'Violation Name': 'privileged-container', 'Violation Category': 'SecurityContext'}, {
            'Violation Name': 'share-host-network-container', 'Violation Category': 'SecurityContext'}, {'Violation Name': 'container-sys-admin-cap-added', 'Violation Category': 'SecurityContext'}]}}
        expected = "\n".join(['| key   | key2   | Violation Name                | Violation Category   |',
                              '|-------+--------+-------------------------------+----------------------|',
                              '| value | value2 | privileged-container          | SecurityContext      |',
                              '| value | value2 | share-host-network-container  | SecurityContext      |',
                              '| value | value2 | container-sys-admin-cap-added | SecurityContext      |'])
        assert violations.pritify() == expected

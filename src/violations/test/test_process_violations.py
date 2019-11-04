import pytest
import json
import os
from violations.process_violations import ProcessViolations
from violations.violations_list import ViolationsList
from violations.violations_summary import ViolationsSummary
from pytest_mock import mocker


FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'data/',
)

DATA = {
    'single_resource_change': os.path.join(FIXTURE_DIR, 'single_resource_output.json'),
    'no_resource_change': os.path.join(FIXTURE_DIR, 'no_changes_output.json')
}


def load_test_data(file):
    f = open(DATA[file], "r")
    return json.loads(f.read())


@pytest.fixture()
def new_file_violations_instance():
    return ProcessViolations()


def test_run_return_instances(new_file_violations_instance, mocker):
    " Mock run_octactl to return full mocked data "
    mocker.patch("violations.process_violations.octactl", return_value=load_test_data('single_resource_change'))
    fv_run = new_file_violations_instance.run()
    assert isinstance(new_file_violations_instance, ProcessViolations)
    assert isinstance(fv_run, ProcessViolations)
    assert isinstance(fv_run.summary, ViolationsSummary)
    assert isinstance(fv_run.violations_list, ViolationsList)


def test_run_empty_octactl_results(new_file_violations_instance, mocker):
    " Mock run_octactl to return empty mocked data "
    mocker.patch("violations.process_violations.octactl",  return_value=load_test_data('no_resource_change'))
    fv_run = new_file_violations_instance.run()
    assert isinstance(fv_run, ProcessViolations)

import pytest
import json
from cmd_run.octactl import Octactl
from violations.process_violations import ProcessViolations
from violations.violations_list import ViolationsList
from violations.violations_summary import ViolationsSummary
from pytest_mock import mocker


# TODO change path to relative
DATA = {
    'single_resource_change': 'src/test/data/single_resource_ourput.json',
    'no_resource_change': 'src/test/data/single_resource_ourput.json'
}


def load_test_data(file):
    f = open(DATA[file], "r")
    return json.loads(f.read())


@pytest.fixture()
def new_file_violations_instance(mocker):
    config = mocker.Mock()
    return ProcessViolations(config)


def test_run_return_instances(new_file_violations_instance, mocker):
    " Mock _runOctactl to return full mocked data "
    mocker.patch.object(Octactl, "run", return_value=load_test_data('single_resource_change'))
    fv_run = new_file_violations_instance.run()
    assert isinstance(new_file_violations_instance, ProcessViolations)
    assert isinstance(fv_run, ProcessViolations)
    assert isinstance(fv_run.summary, ViolationsSummary)
    assert isinstance(fv_run.violations_list, ViolationsList)


def test_run_empty_octactl_results(new_file_violations_instance, mocker):
    " Mock _runOctactl to return empty mocked data "
    mocker.patch.object(Octactl, "run", return_value=load_test_data('no_resource_change'))
    fv_run = new_file_violations_instance.run()
    assert isinstance(fv_run, ProcessViolations)

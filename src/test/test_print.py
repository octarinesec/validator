import pytest
from pytest_mock import mocker
from print_result import print_results, DEFAULT_RAW_SIZE, SUCCESS_MESSAGE


@pytest.fixture
def print_with_result(mocker):
    """ The expected result for this setup should look like: 
    #################################
    #        Result Summary:        #
    #################################
    Shorter text
    #################################




    #################################
    #      Violations Details:      #
    #################################
    Some summary table should be here
    #################################


    """
    config = mocker.MagicMock()
    violation = mocker.MagicMock()
    violation.summary.get = mocker.MagicMock(return_value=["not,empty"])
    violation.violations_list.pritify = mocker.MagicMock(return_value="Some detailed table should be here")
    violation.summary.pritify = mocker.MagicMock(return_value="Shorter text")
    return print_results(config, violation).split('\n')


def test_print_results_with_no_violations(mocker):
    config = mocker.MagicMock()
    violation = mocker.MagicMock()
    violation.summary.get = mocker.MagicMock(return_value=[])
    rst = print_results(config, violation).split('\n')
    assert len(rst[0]) == DEFAULT_RAW_SIZE
    assert len(rst[1]) == DEFAULT_RAW_SIZE
    assert SUCCESS_MESSAGE in rst[1]


def test_print_results_with_violatoin_header_footer_size(print_with_result):
    assert len(print_with_result[0]) == len("Some summary table should be here")

import pytest
from pytest_mock import mocker
from print_result import print_results, DEFAULT_ROW_SIZE, SUCCESS_MESSAGE


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
    violation = mocker.MagicMock()
    violation.empty = False
    v_list = mocker.MagicMock()
    v_list.pritify = mocker.MagicMock(return_value="Some detailed table should be here")
    v_list.data = ["Some detailed table should be here"]
    v_list.headline = "Violations Details:"
    v_sum = mocker.MagicMock()
    v_sum.data["Shorter text"]
    v_sum.headline = "Result Summary:"
    violation.violations_list = v_list
    violation.summary = v_sum
    violation.displayable = [v_list, v_sum]
    return print_results(violation).split('\n')


@pytest.fixture
def print_with_no_result(mocker):
    """ The expected result for this setup should look like
    ####################################################################################################
    #                                      No Violations Detected                                      #
    ####################################################################################################
    """
    violation = mocker.MagicMock()
    violation.summary.get = mocker.MagicMock(return_value=[])
    return print_results(violation).split('\n')


def test_print_results_header_footer_with_no_violations(print_with_no_result):
    assert len(print_with_no_result[0]) == DEFAULT_ROW_SIZE
    assert len(print_with_no_result[-1]) == DEFAULT_ROW_SIZE


def test_print_results_message_with_no_violations(print_with_no_result):
    assert SUCCESS_MESSAGE in print_with_no_result[1]


def test_print_results_with_violations_structure(print_with_result):
    print(print_with_result)
    " 4th line should be footer"
    assert "######" in print_with_result[4]
    " 5th  and 6th should be newline "
    assert "" in print_with_result[5]
    " Last line should be new line"
    assert "" in print_with_result[-1]


def test_print_results_with_violations_center_alignment(print_with_result):
    assert len(print_with_result[1]) == len(print_with_result[0]) - 1

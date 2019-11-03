SUCCESS_MESSAGE = "No Violations Detected"
DEFAULT_ROW_SIZE = 100


def print_results(config, violations):
    result = []
    if len(violations.summary.get()) == 0:
        result.extend(_wrap_text(DEFAULT_ROW_SIZE, _text(SUCCESS_MESSAGE, DEFAULT_ROW_SIZE)))
    else:
        " Set the size of the header and footer by the number of charters in the violation table "
        v_list = violations.violations_list.pritify()
        row_size = len(v_list.split("\n")[0])
        " Set the summary section "
        result.extend(_wrap_text(row_size, _text("Result Summary:", row_size)))
        result.extend(violations.summary.pritify().split('\n'))
        result.extend([_header_footer(row_size), "\n", "\n"])
        " Set the details section "
        result.extend(_wrap_text(row_size, _text("Violations Details:", row_size)))
        result.extend(v_list.split("\n"))
        result.extend([_header_footer(row_size), "\n", "\n"])
    return '\n'.join(result)


def _wrap_text(row_size, text):
    return[_header_footer(row_size), text, _header_footer(row_size)]


def _header_footer(row_size):
    return "#" * row_size


def _text(text, row_size):
    spaces = "".join([" " for x in range(int((row_size - (len(text)+2)) / 2))])
    return ("#{}{}{}#".format(spaces, text, spaces))

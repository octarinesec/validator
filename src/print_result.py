SUCCESS_MESSAGE = "No Violations Detected"
DEFAULT_RAW_SIZE = 100


def print_results(config, violations):
    result = []
    if len(violations.summary.get()) == 0:
        result.extend(_wrap_text(DEFAULT_RAW_SIZE, _text(SUCCESS_MESSAGE, DEFAULT_RAW_SIZE)))
    else:
        " Set the size of the header and footer by the number of charters in the largest column "
        v_list = violations.violations_list.pritify()
        raw_size = len(v_list.split("\n")[0])
        " Set the summary section "
        result.extend(_wrap_text(raw_size, _text("Result Summary:", raw_size)))
        result.extend(violations.summary.pritify().split('\n'))
        result.extend([_header_footer(raw_size), "\n", "\n"])
        " Set the details section "
        result.extend(_wrap_text(raw_size, _text("Violations Details:", raw_size)))
        result.extend(v_list.split("\n"))
        result.extend([_header_footer(raw_size), "\n", "\n"])
    return '\n'.join(result)


def _wrap_text(raw_size, text):
    return[_header_footer(raw_size), text, _header_footer(raw_size)]


def _header_footer(raw_size):
    return "".join(["#" for x in range(raw_size)])


def _text(text, raw_size):
    spaces = "".join([" " for x in range(int((raw_size - (len(text)+2)) / 2))])
    return ("#{}{}{}#".format(spaces, text, spaces))

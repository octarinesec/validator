from functools import wraps
SUCCESS_MESSAGE = "No Violations Detected"
DEFAULT_ROW_SIZE = 100


def print_results(violations):
    result = []
    if len(violations.summary.get()) == 0:
        t = TextWrapper(DEFAULT_ROW_SIZE)
        result.extend(t.headline(SUCCESS_MESSAGE))
    else:
        " Set the size of the header and footer by the number of charters in the violation table "
        v_list = violations.violations_list.pritify()
        row_size = len(v_list.split("\n")[0])
        t = TextWrapper(row_size)
        " Set the summary section "
        result.extend(block(t, "Result Summary:", violations.summary.pritify().split('\n')))
        " Set the details section "
        result.extend(block(t, "Violations Details:", v_list.split("\n")))
        " Set the Error section"
    return '\n'.join(result)


def block(t_hander, headline_text, data):
    r = []
    r.extend(t_hander.headline(headline_text))
    r.extend(data)
    r.extend([t_hander.line, "\n", "\n"])
    return r


class TextWrapper():
    def __init__(self, row_size):
        self.row_size = row_size

    @property
    def line(self):
        return "#" * self.row_size

    def wrapped_text(self, text):
        spaces = "".join([" " for x in range(int((self.row_size - (len(text)+2)) / 2))])
        return ("#{}{}{}#".format(spaces, text, spaces))

    def headline(self, headline_text):
        return [self.line, self.wrapped_text(headline_text), self.line]

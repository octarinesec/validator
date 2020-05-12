from functools import wraps
SUCCESS_MESSAGE = "No Violations Detected"
DEFAULT_ROW_SIZE = 100


def print_results(violations):
    result = []
    if violations.empty:
        t = TextWrapper(DEFAULT_ROW_SIZE)
        result.extend(t.headline(SUCCESS_MESSAGE))
    else:
        # Extract the longes line so it can be used as row_size
        # Currently set statically TODO: Extract it dynamically from the displayables
        v_list = violations.violations_list.pritify()
        row_size = len(v_list.split("\n")[0])
        t = TextWrapper(row_size)
        for item in violations.displayable:
            result.extend(t.headline(item.headline))
            result.extend(item.data)
            result.extend([t.line, "\n", "\n"])
    return '\n'.join(result)


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

import re
from utils import RegPattern
from problems import ProblemLine

#TODO remove method
def show_problem_lines(input_file: str, show_tabs=True):

    pattern = '(?<=[0-9a-zA-Z \\\])"(?=[a-zA-Z0-9 ])'
    # (?< условие до искомого паттеррна)
    # (?= условие после искомого паттеррна)

    patterns = [('^\\s*$', 'The line is empty or contains only whitespace characters.')
            , ('^("",)*""$', 'The line has only empty fields.')
            , ('(\\r|\\n)', 'The line has special symbol like \\n, \\r.')
            , (r'\\', 'The line has backslash.')
            , ('^[^"]', 'The line does not starts with ".')
            , ('[^"]$', 'The line does not ends with ".')
            , (pattern, 'There are additional double quotes in the string.')
            ]
    if show_tabs:
        patterns.append(('\\t', 'The line has special symbol like \\t.'))

    with open(input_file, "r") as ins:
        num = 0
        problem_lines = []
        problem_nums = []
        problem_messages = []
        for line in ins:
            num += 1
            messages = []
            line = line.rstrip()

            for pattern, message in patterns:
                if re.search(pattern, line) is not None:
                    messages.append(message)

            if 2 * int(line.count('"')/2) != line.count('"'):
                messages.append("odd number of quotes in line. ")

            if len(messages) > 0:
                problem_lines.append(line)
                problem_nums.append(num)
                problem_message = " " . join(messages)
                problem_messages.append(problem_message)

    return problem_lines, problem_nums, problem_messages


PATTERTS_LINE_DEFAULT = [(RegPattern.ONLY_BACKSPACE, 'The line is empty or contains only whitespace characters.')
    , ('^("",)*""$', 'The line has only empty fields.')
    , (RegPattern.END_LINE_SYMBOLS, 'The line has special symbol like \\n, \\r.')
    , (RegPattern.BACKSLASH, 'The line has backslash.')
    , (RegPattern.FIRST_SYMBOL_IS_NOT_DBLQUATER, 'The line does not starts with ".')
    , (RegPattern.LAST_SYMBOL_IS_NOT_DBLQUATER, 'The line does not ends with ".')
    , (RegPattern.DBLQUATER_WITH_INCORRECT_SYMBOLS, 'There are additional double quotes in the string.')
    , (RegPattern.ONLY_BACKSPACE, 'The line has special symbol like \\t.')
            ]


def show_problems_in_line(line: str, patterns_with_message=PATTERTS_LINE_DEFAULT):
    messages = []
    for pattern, message in patterns_with_message:
        if re.search(pattern, line) is not None:
            messages.append(message)

    if 2 * int(line.count('"') / 2) != line.count('"'):
        messages.append("odd number of quotes in line. ")
    message = " ".join(messages) if len(messages) > 0 else ''
    return message


def show_problem_lines_v2(input_file: str, is_first_line_header=True, patterns_with_message=PATTERTS_LINE_DEFAULT):
    problem_line = ProblemLine()
    with open(input_file, "r") as fr:
        line_num = 0
        for line in fr:
            line_num += 1
            if line_num == 1 and is_first_line_header:
                continue
            line = line.rstrip()
            problem_message = show_problems_in_line(line, patterns_with_message)
            if problem_message:
                problem_line.add_problem(line_num, line, problem_message)
    return problem_line

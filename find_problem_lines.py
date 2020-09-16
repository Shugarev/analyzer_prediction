import re
from utils import RegPattern

def show_problem_line(input_file: str, show_tabs=True):

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


def show_problem_line_v2(input_file: str, is_first_line_header=True, is_print_problem=True,
                         patterns_with_message=PATTERTS_LINE_DEFAULT):

    with open(input_file, "r") as fr:
        line_num = 0
        problem_lines = []
        problem_lines_num = []
        problem_messages = []
        for line in fr:
            line_num += 1
            if line_num == 1 and is_first_line_header:
                continue
            line = line.rstrip()
            messages = []
            for pattern, message in patterns_with_message:
                if re.search(pattern, line) is not None:
                    messages.append(message)

            if 2 * int(line.count('"')/2) != line.count('"'):
                messages.append("odd number of quotes in line. ")

            if len(messages) > 0:
                problem_lines.append(line)
                problem_lines_num.append(line_num)
                problem_message = " " . join(messages)
                problem_messages.append(problem_message)
                if is_print_problem:
                    print(' problem_lines_num: ' + str(line_num))
                    print(' problem message: ' + problem_message)
                    print(' problem line: \n' + line)

    return {'problem_lines': problem_lines,
             'problem_lines_num': problem_lines_num,
             'problem_messages': problem_messages}

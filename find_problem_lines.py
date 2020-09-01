import re


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


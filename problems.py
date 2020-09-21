import re
import numpy as np
import pandas as pd


class ProblemLine:
    def __init__(self, nums=[], lines=[], messages=[]):
        self.nums = nums
        self.lines = lines
        self.messages = messages

    def get_problem_data(self)->dict:
        data = {'num': self.nums
            , 'line': self.lines
            , 'message': self.messages
                }
        return data

    def get_problem_df(self) -> pd.DataFrame:
        data = self.get_problem_data()
        dt = pd.DataFrame.from_dict(data)
        return dt

    def add_problem(self, num, line, message):
        if message is list:
            message = " ".join(message) if len(message) > 0 else ''

        self.nums.append(num)
        self.lines.append(line)
        self.messages.append(message)

    def get_problems_df_mask(self, column='line', pattern='NULL') -> pd.DataFrame:
        dt = self.get_problem_df()
        dt_sub = dt[dt.loc[:, column].apply(lambda x: not pd.isna(x) and not bool(re.search(pattern, x)))]
        return dt_sub

    def print_problems(self, is_print):
        '''
            0 - don't print
            1 - print all error
            2 - print all error except NULL fields
        :return:
        '''
        n = len(self.messages)
        nums = self.nums
        lines = self.lines
        messages = self.messages
        for i in range(n):
            print("num:" + str(nums[i]))
            print("line:" + str(lines[i]))
            print("message" + str(messages[i]))

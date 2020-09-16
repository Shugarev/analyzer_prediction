import pandas as pd
import json
import re
from utils import RegPattern


def _get_one_column_from_json(x: str, col_name: str):
    '''
     :example
     x = '{"client":{"phone":"923143****", "name":"Наталья Алтынбаева", "email":"aa49@mail.ru"}}'
     col_name = 'client.phone'
      _get_one_column_from_json(x,col_name) -> "923143****"
    '''
    try:
        d = json.loads(x)
        flat_dictionary = Converter.get_flat_dictionary(d)
        ret_val = flat_dictionary[col_name]
    except:
        ret_val = ''
    return ret_val


class Converter:
    @classmethod
    def get_flat_dictionary(cls, item, old_key=None) -> dict:
        '''
        :param  item - dict, list or str
                old_key concatenated key:
        :return flat dict:
        :example
            item = {'client': {'phone': '923143****', 'name': 'Наталья Алтынбаева', 'email': 'aa49@mail.ru'}}
            get_flat_dictionary(cls, item, old_key=None)
         :return
            {'client.phone': '923143****', 'client.name': 'Наталья Алтынбаева', 'client.email': 'aa49@mail.ru'}
        '''
        flat_dic = {}
        if isinstance(item, dict):
            for key, value in item.items():
                new_key = old_key + '.' + key if old_key is not None else key
                flat_dic.update(cls.get_flat_dictionary(value, new_key))
        elif isinstance(item, list):
            key = 1
            for value in item:
                new_key = old_key + '.' + str(key) if old_key is not None else key
                flat_dic.update(cls.get_flat_dictionary(value, new_key))
                key += 1
        else:
            flat_dic = {old_key: item}
        return flat_dic

    @classmethod
    def merge_flat_dictionary_keys_from_json_column(cls, dt: pd.DataFrame, col_name: str, is_print_error=0) -> list:
        '''
        params:
            is_print_error
            0 - don't print
            1 - print all error
            2 - print all error except NULL fields
        example:
            data_json = [{"client":{"phone":"923143****", "email":"aaaaaa49@mail.ru"}},
                        {"order":{"id":"111111111"}, "client":{"email":"aaaa@gmail.com"}}]

            df = pd.DataFrame(data={"json":data_json})
            col_name = 'json'
            Converter.merge_flat_dictionary_keys_from_json_column(df, col_name)
        return:
            ['client.phone', 'order.id', 'client.email']
             Порядок полей в листе может быть разный
        '''
        n = dt.shape[0]
        col_names = []
        column_values = dt[col_name].tolist()

        for i in range(n):
            json_load = column_values[i]
            try:
                d = json.loads(json_load)
                flat_dic = cls.get_flat_dictionary(d)
            except:
                if is_print_error == 1:
                    print("col num =" + str(i))
                    print(json_load)
                elif is_print_error == 2 and json_load != "NULL":
                    print("col num =" + str(i))
                    print(json_load)
                flat_dic = {}

            col_names = list(set(col_names + list(flat_dic.keys())))
        return col_names

    @classmethod
    def write_json_column_to_csv(cls, dt: pd.DataFrame, col_name: str, col_names: list, output_file: str,
                                 is_print_error=0):
        '''
        params:
            is_print_error
            0 - don't print
            1 - print all error
            2 - print all error except NULL fields
        example:
            data_json = [{"client":{"phone":"923143****", "email":"aaaaaa49@mail.ru"}},
                        {"order":{"id":"111111111"}, "client":{"email":"aaaa@gmail.com"}}]

            df = pd.DataFrame(data={"json":data_json})
            col_name = "json"
            col_names = ['client.phone', 'client.email']
            Converter.write_json_column_to_csv(df, col_name, col_names, output_file)
        return:
            ['"client.phone","client.email"\n"923143****","aaaaaa49@mail.ru"\n"","aaaa@gmail.com"\n']
        '''
        fw = cls.write_head_to_file(col_names, output_file)

        n = dt.shape[0]
        column_values = dt[col_name].tolist()
        full_flat_dic = {str(key): "" for key in col_names}

        default_csv_line = cls.get_default_csv_line(col_names)

        for line_number in range(n):
            json_load = column_values[line_number]
            csv_line = cls.get_csv_line_from_json(col_names,  default_csv_line, full_flat_dic, json_load, line_number,
                                                  is_print_error)
            fw.write(csv_line + "\n")

        fw.close()

    @classmethod
    def write_head_to_file(cls, col_names, output_file):
        '''
        example:
            col_names = ["order.location", "client.email"]
        result: ['"order.location","client.email"\n'] -> in output file
        '''
        fw = open(output_file, 'w')
        csv_line = '"' + '","'.join(col_names) + '"'
        fw.write(csv_line + "\n")
        return fw

    @classmethod
    def convert_one_column_from_json(cls, dt, col_json_name, col_name) -> pd.Series:
        '''
        example:
            data_json = [{"client":{"phone":"923143****", "email":"aaaaaa49@mail.ru"}},
                        {"order":{"id":"111111111"}, "client":{"email":"aaaa@gmail.com"}}]

            df = pd.DataFrame(data={"json":data_json})
            col_json = 'json'

            Converter.convert_one_column_from_json(df, col_json, 'client.email')
        return:
            pd.Series({0: 'aaaaaa49@mail.ru', 1: 'aaaa@gmail.com'})

            Converter.convert_one_column_from_json(df, col_json, 'order.id')
        return_2:
            pd.Series({0: '', 1: '111111111'})
        '''
        return dt[col_json_name].apply(lambda x: _get_one_column_from_json(x, col_name))

    @classmethod
    def correct_json_load(cls, json_load: str)->str:
        '''
        :example
        json_load = '{"is_trailer":false,"user_agent":"Mozilla/5.0 rv:52.0", "has_middle_name ":true,
         "insurance_selected":null}'
         correct_json_load(cls, json_load)
         :return '{"is_trailer":"false","user_agent":"Mozilla/5.0 rv:52.0", "has_middle_name ":"true",
         "insurance_selected":"null"}'

         add adds extra quotes: rv:52.0->rv:"52.0"
         json_load = re.sub(RegPattern.WORD_AFTER_COLON, ':"\\1"', str(json_load))
        '''

        json_load = re.sub(':\s*true', ':"true"', json_load)
        json_load = re.sub(':\s*false', ':"false"', json_load)
        json_load = re.sub(':\s*null', ':"null"', json_load)
        return json_load

    @classmethod
    def write_json_column_to_csv_read_data_from_file(cls, input_file: str, col_names: list, output_file: str,
                                                     is_print_error=0):
        '''
        params:
            is_print_error
            0 - don't print
            1 - print all error
            2 - print all error except NULL fields

        example:
            input_file.csv:
            order_id		json
            45195195728489703	{"client":{"phone":"923143****", "email":"aaaaaaaa_aaaaaaa_2018@mail.ru\\n"}}
            46462306263175020	{"order":{"location":"ЧУП \\"Самелго-Плюс\\" Сак"},"client":{"email":"aaaa@gmail.com"}}

            col_names = ["order.location", "client.email"]
            Converter.write_json_column_to_csv_read_data_from_file(self.input_file, col_names, self.output_file)

        output_file.csv:
            "order.location","client.email"
            "","aaaaaaaa_aaaaaaa_2018@mail.ru"
            "ЧУП Самелго-Плюс Сак","aaaa@gmail.com"
        '''
        fw = cls.write_head_to_file(col_names, output_file)
        default_csv_line = cls.get_default_csv_line(col_names)

        full_flat_dic = {str(key): "" for key in col_names}
        problems = []
        problem_lines = []
        problem_nums = []

        with open(input_file) as fr:
            line = fr.readline()
            line_number = 1
            while line:
                if line_number > 1:
                    result = re.search(RegPattern.JSON_LINE, line)
                    if result:
                        json_load = result.group(0)
                        cls.find_problems_line(json_load, line_number, problem_lines, problem_nums, problems)

                        json_load = cls.update_json_by_pattern(json_load)

                        json_load = cls.correct_json_load(json_load)

                        csv_line = cls.get_csv_line_from_json(col_names,  default_csv_line, full_flat_dic,
                                                              json_load, line_number, is_print_error)
                    else:
                        csv_line = cls.not_extracted_json_col_by_regexp(default_csv_line, line, line_number,
                                                                        problem_lines, problem_nums, problems,
                                                                        is_print_error)
                    fw.write(csv_line + "\n")

                line_number += 1
                line = fr.readline()

        return {"problem_lines": problem_lines, "problem": problems, "problem_nums": problem_nums}

    @classmethod
    def get_default_csv_line(cls, col_names):
        '''
        example:
            col_names = ["order.location", "client.email"]
        result: '"",""' -> for empty df rows
        '''
        default_list = [""] * len(col_names)
        default_csv_line = '"' + '","'.join(default_list) + '"'
        return default_csv_line

    @classmethod
    def not_extracted_json_col_by_regexp(cls, default_csv_line, line, line_number, problem_lines,
                                         problem_nums, problems, is_print_error=0):
        problem = 'does not pares json field'
        problems.append(problem)
        problem_lines.append(line)
        problem_nums.append(line_number)
        if is_print_error == 1:
            print(problem)
            print(line_number)
            print(line)
        elif not str(line).startswith("NULL") and is_print_error == 2:
            print(problem)
            print(line_number)
            print(line)
        return default_csv_line

    @classmethod
    def get_csv_line_from_json(cls, col_names, default_csv_line, full_flat_dic, json_load, line_number, is_print_error=0):
        try:
            d = json.loads(json_load)
            flat_dic = cls.get_flat_dictionary(d)
            flat_dic = {**full_flat_dic, **flat_dic}
            col_names_values = [str(flat_dic[col]) for col in col_names]
            csv_line = '"' + '","'.join(col_names_values) + '"'
        except:
            if is_print_error == 1:
                print("col num =" + str(line_number))
                print(json_load)
            elif is_print_error == 2 and json_load != "NULL":
                print("col num =" + str(line_number))
                print(json_load)
            csv_line = default_csv_line
        return csv_line

    @classmethod
    def find_problems_line(cls, json_load, line_number, problem_lines, problem_nums, problems):
        problem = re.findall(RegPattern.BACKSLASH_IN_LINE, json_load)
        if len(problem) > 0:
            problems += problem
            problem_lines.append(str(json_load))
            problem_nums.append(line_number)

    @classmethod
    def update_json_by_pattern(cls, json_load: str) -> str:
        '''
        example :
            patterns = '{"is\\\\\\\\":"\\\\"fal\\\\nse","u\\\\tser_agen\\\\bt":"Mo\\\\,zilla/5.0 rv:52.0"}'
        result: '{"is ":"false","user_agent":"Mo,zilla/5.0 rv:52.0"}'
        '''
        json_load = re.sub(RegPattern.BACKSLASH_4, ' ', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_n, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_t, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_b, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_DBLQUATER, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_COMA, ',', json_load)
        return json_load

    @classmethod
    def is_problem_line(cls, line):
        '''
        :example
            line = '{"train":{"is_trailer":false,"is_firm":false, "email":shugarev@gmail.com}}'
        result: 1
        :example 2
            line = '{"train":{"is_trailer":false,"is_firm":true, "email":null}}'
        result 2: 0
        '''
        pattern = ':([a-zA-Z]+)'
        incorrect_values = {'true', 'false', 'null'}
        incorrect_values_in_line = set(re.findall(pattern, line))
        diff = incorrect_values_in_line.difference(incorrect_values)
        return len(diff)

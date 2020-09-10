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
    def get_flat_dictionary(cls, item, old_key=None)->dict:
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
                key = key + 1
        else:
            flat_dic = {old_key: item}
        return flat_dic

    @classmethod
    def merge_flat_dictionary_keys_from_json_column(cls, dt: pd.DataFrame, col_name: str)->list:
        '''
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
                print("col num =" + str(i))
                print(json_load)
                flat_dic = {}

            col_names = col_names + list(flat_dic.keys())
            col_names = set(col_names)
            col_names = list(col_names)
        return col_names

    @classmethod
    def write_json_column_to_csv(cls, dt: pd.DataFrame, col_name: str, col_names: list, output_file: str):
        '''
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
        fw = open(output_file, 'w')
        csv_line = '"' + '","'.join(col_names) + '"'
        fw.write(csv_line + "\n")

        n = dt.shape[0]
        column_values = dt[col_name].tolist()
        full_flat_dic = {str(key): "" for key in col_names}

        default_list = [""] * len(col_names)
        default_csv_line = '"' + '","'.join(default_list) + '"'

        for i in range(n):
            json_load = column_values[i]
            try:
                d = json.loads(json_load)
                flat_dic = cls.get_flat_dictionary(d)
                flat_dic = {**full_flat_dic, **flat_dic}
                col_names_values = [str(flat_dic[col]) for col in col_names]
                csv_line = '"' + '","'.join(col_names_values) + '"'
            except:
                print("col num =" + str(i))
                print(json_load)
                csv_line = default_csv_line

            fw.write(csv_line + "\n")

        fw.close()

    @classmethod
    def convert_one_column_from_json(cls, dt, col_json_name, col_name)-> pd.Series:
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
    def write_json_column_to_csv_read_data_from_file(cls, input_file: str, col_names: list, output_file: str):
        '''
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
        fw = open(output_file, 'w')
        csv_line = '"' + '","'.join(col_names) + '"'
        fw.write(csv_line + "\n")

        default_list = [""] * len(col_names)
        default_csv_line = '"' + '","'.join(default_list) + '"'

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

                        problem = re.findall(RegPattern.BACKSLASH_IN_LINE, json_load)
                        if len(problem) > 0:
                            problems = problems + problem
                            problem_lines.append(json_load)
                            problem_nums.append(line_number)

                        # extract method
                        json_load = cls.update_json_by_pattern(json_load)
                        json_load = re.sub(RegPattern.WORD_AFTER_COLON, ':"\\1"', str(json_load))
                        #  generic code
                        try:
                            d = json.loads(json_load)
                            flat_dic = cls.get_flat_dictionary(d)
                            flat_dic = {**full_flat_dic, **flat_dic}
                            col_names_values = [str(flat_dic[col]) for col in col_names]
                            csv_line = '"' + '","'.join(col_names_values) + '"'
                        except:
                            print("col num =" + str(line_number))
                            print(json_load)
                            csv_line = default_csv_line

                    else:

                        problems.append(problem)
                        problem_lines += line
                        problem_nums.append(line_number)

                        csv_line = default_csv_line
                        print('does not pares json field')
                        print(line_number)
                        print(line)
                    fw.write(csv_line + "\n")

                line_number += 1

                line = fr.readline()

        return problem_lines, problems, problem_nums

    @classmethod
    def update_json_by_pattern(cls, json_load: str) -> str:
        json_load = re.sub(RegPattern.BACKSLASH_4, ' ', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_n, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_t, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_b, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_DBLQUATER, '', json_load)
        json_load = re.sub(RegPattern.BACKSLASH_2_COMA, ',', json_load)
        return json_load



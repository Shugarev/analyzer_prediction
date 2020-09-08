import pandas as pd
import json


def convert_one_column_from_json(x: str, col_name: str):
    try:
        d = json.loads(x)
        flat_dictionary = Converter.get_flat_dictionary(d)
    except:
        return ''
    return flat_dictionary[col_name]

class Converter:

    @classmethod
    def get_flat_dictionary(cls, item, old_key=None)->dict:
        '''
        :param  item - dict, list or str
                old_key concatenated key:
        :return flat dict:
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
                # key = key + 1
        else:
            flat_dic = {old_key: item}
        return flat_dic

    @classmethod
    def get_flat_dictionary_col_names(cls, dt: pd.DataFrame, col_name: str)->list:
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

        return dt[col_json_name].apply(lambda x: convert_one_column_from_json(x, col_name))



import os, inspect
import pandas as pd


class DataForTests:

    w = {"ID": ["414720******4963_2019-11", "441103******6134_2021-07", "434769******7655_2021-10"]}
    white = pd.DataFrame(data=w)

    data = {'id': ["427082******7013_2023-03", "414720******4963_2019-11", "434769******7655_2021-10"
        , "434769******7655_2021-10", "407204******7425_2020-12", "483316******8724_2021-03", "483316******8724_2021-03"
        , "406032******1745_2021-07", "406032******1745_2021-07", "441103******6134_2021-07"]
        , 'status': [1, 0, 1, 1, 0, 0, 0, 0, 1, 0]
        , 'amount': ["264.75", "205.90", "22.24", "22.24", "42.36", "26.48", "31.77", "21.18", "21.18", "52.95"]
        , 'bin': ['510250', '510211', '510250', '510211', '510250', '510211', '510260', '510260', '510260', '510260']
        , 'probability': [0.96, 0.83, 0.24, 0.37, 0.48, 0.74, 0.51, 0.21, 0.76, 0.61]
            }

    date = ['2019-11-20 09:39:36', '2019-11-21 10:39:36', '2019-11-27 03:49:36', '2019-11-29 19:39:36'
        , '2019-12-02 09:39:36', '2019-12-07 23:39:36', '2019-12-17 11:39:36', '2019-12-23 09:39:36'
        , '2019-12-24 08:39:36', '2019-12-25 14:39:36']

    db_teach = pd.DataFrame(data=data)

    db_teach_with_date = db_teach.copy()
    db_teach_with_date['date'] = date

    db_test = pd.DataFrame(data=data.copy())
    db_test["probability"] = pd.to_numeric(db_test["probability"], errors="coerce")
    db_test["amount"] = pd.to_numeric(db_test.amount, errors="coerce")

    COL_NAMES = ['description', 'p_1', 'p_2', 'p_3', 'p_4', 'p_5', 'p_6', 'p_7', 'p_10', 'p_20', 'rating'
        , 'n_white_list', 'n_test_in_wl', 'n_test_bad_in_wl', 'amount_test_in_wl', 'amount_test_bad_in_wl'
        , 'n_teach', 'n_teach_bad', 'n_test', 'n_test_bad', 'amount_test_bad', 'amount_test']

    EXPECTED_ROW = {'amount_test': 711.04999999999995, 'amount_test_bad': 330.41000000000003
        , 'amount_test_bad_in_wl': 589.25999999999999, 'amount_test_in_wl': 303.33000000000004
        , 'description': 'Test1', 'n_teach': 10, 'n_teach_bad': 4, 'n_test': 10, 'n_test_bad': 4
        , 'n_test_bad_in_wl': 6, 'n_test_in_wl': 4, 'n_white_list': 3}

    DB_TEST = {'id': {0: '427082******7013_2023-03', 8: '406032******1745_2021-07', 5: '483316******8724_2021-03'
            , 6: '483316******8724_2021-03', 4: '407204******7425_2020-12', 7: '406032******1745_2021-07'
            , 1: '414720******4963_2019-11', 2: '434769******7655_2021-10', 3: '434769******7655_2021-10'
            , 9: '441103******6134_2021-07'}
        , 'status': {0: 1, 8: 1, 5: 0, 6: 0, 4: 0, 7: 0, 1: 0, 2: 1, 3: 1, 9: 0}
        , 'amount': {0: 264.75, 8: 21.18, 5: 26.48, 6: 31.77, 4: 42.36, 7: 21.18, 1: 205.9, 2: 22.24, 3: 22.24,
                     9: 52.95}
        , 'bin': {0: '510250', 8: '510260', 5: '510211', 6: '510260', 4: '510250', 7: '510260', 1: '510211'
            , 2: '510250', 3: '510211', 9: '510260'}
        , 'probability': {0: 0.96, 8: 0.76, 5: 0.74, 6: 0.51, 4: 0.48, 7: 0.21, 1: 0.0, 2: 0.0, 3: 0.0, 9: 0.0}
        , 'cum_amount': {0: 264.75, 8: 285.93, 5: 312.41, 6: 344.18, 4: 386.54, 7: 407.72, 1: 613.62, 2: 635.86
        , 3: 658.1, 9: 711.0500000000001}}

    EXPECTED_RESULT_DF = {'description': {0: 'Test1', 1: 'threshold count'}, 'p_1': {0: 0.0, 1: 0.0},
                          'p_2': {0: 0.0, 1: 0.0}, 'p_3': {0: 0.0, 1: 0.0}, 'p_4': {0: 0.0, 1: 0.0},
                          'p_5': {0: 0.0, 1: 0.0}, 'p_6': {0: 25.0, 1: 0.96}
        , 'p_7': {0: 25.0, 1: 0.96}, 'p_10': {0: 25.0, 1: 0.96}, 'p_20': {0: 50.0, 1: 0.76},
                          'rating': {0: 75.0, 1: 75.0}
        , 'n_white_list': {0: 3, 1: 3}, 'n_test_in_wl': {0: 4, 1: 4}, 'n_test_bad_in_wl': {0: 6, 1: 6}
        , 'amount_test_in_wl': {0: 303.33000000000004, 1: 303.33000000000004}
        , 'amount_test_bad_in_wl': {0: 589.26, 1: 589.26}, 'n_teach': {0: 10, 1: 10}, 'n_teach_bad': {0: 4, 1: 4}
        , 'n_test': {0: 10, 1: 10}, 'n_test_bad': {0: 4, 1: 4}, 'amount_test_bad': {0: 330.41, 1: 330.41}
        , 'amount_test': {0: 711.05, 1: 711.05}}

    EXPECTED_STAT_DT = {'n': {'510211': 3, '510250': 3, '510260': 4}
        , 'amount_total': {'510211': 254.62, '510250': 329.35, '510260': 127.08}
        , 'n_bad': {'510211': 1, '510250': 2, '510260': 1}
        , 'amount_bad': {'510211': 22.24, '510250': 286.99, '510260': 21.18}
        , 'cb_rate': {'510211': 33.3333, '510250': 66.6667, '510260': 25.0}
        , 'cb_rate_amount': {'510211': 8.7346, '510250': 87.1383, '510260': 16.6667}
        , 'true_amount_weight': {'510211': 0.07882499894444649, '510250': 0.8702098888735693,
                                 '510260': 0.0756564702066755}
        , 'false_amount_weight': {'510211': 0.6137171323460444, '510250': 0.11863099642533326,
                                  '510260': 0.28418079684845704}
        , 'true_weight': {'510211': 0.4, '510250': 0.6, '510260': 0.4}
        , 'false_weight': {'510211': 0.42857142857142855, '510250': 0.2857142857142857, '510260': 0.5714285714285714}
        , 'p': {'510211': 0.48275862068965525, '510250': 0.6774193548387096, '510260': 0.411764705882353}
        , 'p_a': {'510211': 0.11381978854855095, '510250': 0.8800302473441175, '510260': 0.2102519031056441}}

    EXPECTED_STAT_DT_WITH_DATE = EXPECTED_STAT_DT.copy()

    min_date = {'510211': '2019-11-21 10:39:36', '510250': '2019-11-20 09:39:36', '510260': '2019-12-17 11:39:36'}
    max_date = {'510211': '2019-12-07 23:39:36', '510250': '2019-12-02 09:39:36', '510260': '2019-12-25 14:39:36'}

    EXPECTED_STAT_DT_WITH_DATE['min'] = min_date
    EXPECTED_STAT_DT_WITH_DATE['max'] = max_date

    #  ----------------------------------------------------------- For Factor -----------------------------------

    data_factor = {'zip': ['56789', '96746', '45x01', '21540590', '1121D', '57075440', 'Rm4606', '020-72', '33015',
                           '32514']
        , 'phone': ['1356789364528', '1086510074', '1002929855', '11994891341', '977852230', '', '7183741', '83292591'
            , '1065951413', '128298821232']
        , 'ip': ['184.56.163.85','204.210.126.255', '99.203.145.83', '69.181.49.246', '179.158.244.208',
                 '166.137.175.69'
            , '172.58.11.54', '174.202.7.127', '99.177.243.220', '73.108.11.150']
        , 'card_masked': ['547087****8523', '517148****4111', '546540****4046', '510805****4554', '544731****8532'
            , '524038****4345', '551791****2736', '517805****4590', '517805****4126', '517805****4536']
        , 'card_holder': ['Gabriele Markes', 'Malia Gusman', 'Stephen Gordy', 'Nicholas Saephanh', 'Thiago Fernandes'
            , 'Jamal Stephens', 'Jorge Hernandez', 'Joseph Rusolo', 'thomas van', 'Micah Pitchford']
        , 'email': ['gabriele@markes.com', 'Fdaret1836@4mail.com.net', 'Vanwerd@4roll.mail', '18888_steven@gmail.com'
            , 'Hardcool12@pochta.net', 'StorestWin@yandex.com', '4334788@gmail.com', '585851@4null.com.ua'
            , 'AwertNord@hotmail.com', 'MerchAS@mail.ru']
        , 'address': ['Saint Brabus AMG 12', '5263 Ihilani place', '2111 Bishop Hill Road', '1502 International Blvd'
            , 'Rua sumidouro 35', '9 Highland St', '18336 NW 68th Ave Apt L', '6317 15th ave'
            , '9100 Baldridge road app 9324', '1204 Texas Avenue']
        }

    db_teach_factor = pd.DataFrame(data=data_factor)

    #  ----------------------------------------------------------- For Converter -----------------------------------

    str_for_converter = '{"client":{"phone":"923143****", "email":"aaaaaa49@mail.ru"}}'
    str_for_converter_2 = '{"order":{"id":"111111111"},"client":{"email":"aaaa@gmail.com"}}'
    df_converter = pd.DataFrame(data={"json": [str_for_converter, str_for_converter_2]})

    is_prb_line = '{"train":{"is_trailer":false,"is_firm":false, "email":shugarev@gmail.com}}'

    str_adds_quotes = '{"is_trailer":false,"user_agent":"Mozilla/5.0 rv:52.0", "has_middle_name ":true,' \
                      '"insurance_selected":null}'

    json_load_for_patterns = '{"is\\\\\\\\":"\\\\"fal\\\\nse","u\\\\tser_agen\\\\bt":"Mo\\\\,zilla/5.0 rv:52.0"}'

    converted_str = {'client': {'phone': '923143****', 'name': 'Наталья Алтынбаева', 'email': 'aa49@mail.ru'}}

    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    intput_file = current_dir + '/input_json_converter.csv'
    output_file = current_dir + '/output_json_converter.txt'
    head_output_file = current_dir + '/head_output_file.txt'
    incorrect_html_file = current_dir + '/incorrect_csv_html.csv'
    correct_html_file = current_dir + '/correct_csv_html.csv'
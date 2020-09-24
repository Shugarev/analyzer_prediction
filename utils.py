

class RegPattern:
    BACKSLASH_4_DBLQUATER = r'\\\\\\\\"'
    BACKSLASH_2_DBLQUATER = r'\\\\"'
    BACKSLASH_2_n = r'\\\\n'
    BACKSLASH_2_t = r'\\\\t'
    BACKSLASH_2_b = r'\\\\b'
    BACKSLASH_2_COMA = r'\\\\,'
    BACKSLASH_4 = r'\\\\\\\\'
    DATE_TIME = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
    ORDER_ID = r"^(\d+)\D"
    AFTER_LAST_CURL_BRACE = r"}[^}]*$"
    BEFORE_FIRST_CURL_BRACE = r"^[^{]*{"

    JSON_LINE = '[{](.+)[}]'
    BACKSLASH_IN_LINE = r'[^"]+\\[^"]+'

    WORD_AFTER_COLON = ':([a-zA-Z]+)'
    '''
    example
    df_correct_line['correct_json'] = df_correct_line.json.apply(lambda x:
                                    re.sub(RegPattern.WORD_AFTER_COLON, ':"\\1"', str(x)))
    {"sms_notification":true, "has_rzd_bonus":false} -> {"sms_notification":"true", "has_rzd_bonus":"false"}
    '''
    FIRST_SYMBOL_IS_NOT_DBLQUATER = r'^[^"]'
    LAST_SYMBOL_IS_NOT_DBLQUATER = r'[^"]$'
    ONLY_BACKSPACE = r'^\s*$'
    BACKSLASH = r'\\'
    DBLQUATER_WITH_INCORRECT_SYMBOLS = '[0-9a-zA-Z \\\]"[a-zA-Z0-9 ]'
    END_LINE_SYMBOLS = '(\\r|\\n)'

class UtilsKy:
    # kyw3
    PATH_KYW3 = '/mnt/files/workdata/work/merchants/merchant_33_kyw3_2020-06-05/'
    PATH_DATA_KYW3 = PATH_KYW3 + '04_experiments/ex_01_some_teach/'
    DB_TEACH_KYW3 = PATH_DATA_KYW3 + 'db_teach_2_digit_status_kyw3_from_2019-11-20_to_2020-03-13.csv'
    DB_TEST_KYW3 = PATH_DATA_KYW3 + 'db_test_2_digit_status_kyw3a_from_2020-04-06_to_2020-05-06.csv'
    PATH_WHITE_KYW3 = '/mnt/files/workdata/work/merchants/merchant_33_kyw3_2020-06-05/08_white_lists/'
    WHITE_KYW3 = PATH_WHITE_KYW3 + 'white_list_kyw3_expeiment1_trusted_2020-02-20.csv'

    # ky9
    PATH_DATA_KY9 = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                    '/ex_05_ky9_xgb_jupiter_2020_07_08/'
    DB_TEACH_KY9 = PATH_DATA_KY9 + 'db_teach_xgb_ky9.csv'
    DB_TEST_KY9 = PATH_DATA_KY9 + 'db_test_xgb_ky9.csv'
    DB_TEACH_KY9_ALL = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa' \
                       '/04_experiments/ex_02_description/db_teach_700th_ky9_2018-12-19_2020-01-12.csv'

    DB_TEACH_KY9_300 = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                       '/ex_02_description/db_teach_1m_ky9_2018-12-19_2020-01-12.csv'

    WHITE_KY9 = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                '/white_lists/white_list_CardMasked_trusted_2019-12-17.csv'

    PATH_DATA_KY9_FOR_PROD = '/mnt/files/workdata/work/merchants/merchant_32_ky9_2020-05-12_white_visa/04_experiments' \
                             '/ex_06_for_prod/'
    DB_TEACH_KY9_FOR_PROD = PATH_DATA_KY9_FOR_PROD + 'db_teach_for_prod_ky9_2018-12-19_2020-04-02.csv'
    DB_TEST_KY9_FOR_PROD = PATH_DATA_KY9_FOR_PROD + 'db_test_for_prod_ky9_2020-04-02_2020-05-12.csv'

    GRAFANA_OPERATIONS = '/mnt/files/workdata/work/merchants/merchant_31_data_for_grafana/02_pure_data/' \
                         'operations_with_am_usd.csv'




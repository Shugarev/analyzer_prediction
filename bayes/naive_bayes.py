import numpy as np
import pandas as pd

from statistic import Statistic

ALL = '__ALL__'


class Bayes:

    def __init__(self, calculation_type='counter'):
        self.calculation_type = calculation_type
        self.is_test_weight = False

    def set_calculation_type(self, calculation_type):
        self.calculation_type = calculation_type

    def get_list_factors(self, col_names):
        if 'status' in col_names:
            col_names.remove('status')
        if 'amount' in col_names:
            col_names.remove('amount')
        return col_names

    def fit(self, db_teach, col_names=ALL):
        db_teach = db_teach.copy()
        model_bayes = {}
        if 'amount' not in list(db_teach):
            db_teach['amount'] = 1

        if col_names.__class__ == str and col_names == ALL:
            col_names = list(db_teach)

        factor_list = self.get_list_factors(col_names)
        print("factor_list = {}".format(factor_list))

        for col in factor_list:
            st = Statistic.get_stat_summarise_by_column(db_teach, col)
            col_good = col + '_fw'
            col_bad = col + '_tw'

            if self.calculation_type == 'counter':
                st.false_weight = np.where(st.n_bad == 0, 1, st.false_weight)
                st.true_weight = np.where(st.n_bad == 0, 1, st.true_weight)
            else:
                st.false_weight = np.where(st.n_bad == 0, 1, st.false_amount_weight)
                st.true_weight = np.where(st.n_bad == 0, 1, st.true_amount_weight)

            data = {col: list(st.index), col_good: st.false_weight.values, col_bad: st.true_weight.values}
            df = pd.DataFrame(data)
            model_bayes[col] = df

        self.model_bayes = model_bayes

    def create_test_weight(self, db_test, col_names=ALL):
        test_weight = db_test.copy()
        if col_names.__class__ == str and col_names == ALL:
            col_names = list(test_weight)

        factor_list = self.get_list_factors(col_names)
        model_bayes = self.model_bayes

        for col in factor_list:
            col_good = col + '_fw'
            col_bad = col + '_tw'

            test_weight = test_weight.merge(model_bayes[col], left_on=col, right_on=col, how='left')

            test_weight[col_good] = np.where(pd.isnull(test_weight[col_good]), 1, test_weight[col_good])
            test_weight[col_bad] = np.where(pd.isnull(test_weight[col_bad]), 1, test_weight[col_bad])

        self.test_weight = test_weight
        self.full_factor_list = factor_list

    def predict_proba(self, col_names=ALL):

        if col_names.__class__ == str and col_names == ALL:
            col_names = self.full_factor_list
        factor_list = self.get_list_factors(col_names)

        test_weight = self.test_weight

        test_weight['true_weight'] = 1
        test_weight['false_weight'] = 1

        for col in factor_list:
            col_good = col + '_fw'
            col_bad = col + '_tw'
            test_weight['true_weight'] = test_weight['true_weight'] * test_weight[col_bad]
            test_weight['false_weight'] = test_weight['false_weight'] * test_weight[col_good]

        test_weight['probs'] = test_weight['true_weight'] / (test_weight['true_weight'] + test_weight['false_weight'])
        classone_probs = test_weight['probs'].values
        classzero_probs = 1.0 - classone_probs
        return np.vstack((classzero_probs, classone_probs)).transpose()

    def get_feature_importance(self, db_teach, col_names=ALL):
        db_teach = db_teach.copy()
        if 'amount' not in list(db_teach):
            db_teach['amount'] = 1

        if col_names.__class__ == str and col_names == ALL:
            col_names = list(db_teach)

        factor_list = self.get_list_factors(col_names)

        feature_importance = []
        n_unique = []

        for f in factor_list:
            st = Statistic.get_stat_summarise_by_column(db_teach, f)
            value = (st.p - 0.5).abs().sum()
            feature_importance.append(value)
            n_unique.append(st.shape[0])

        data = {'feature': factor_list, 'feature_importance': feature_importance, 'n_unique': n_unique}
        df = pd.DataFrame(data)
        df.sort_values(by='feature_importance', ascending=False , inplace=True)
        return df

    def compare_factor_teach_test(self, db_teach, db_test, col_names=ALL):
        db_teach = db_teach.copy()
        db_test = db_test.copy()

        if 'amount' not in list(db_teach):
            db_teach['amount'] = 1
        if 'amount' not in list(db_test):
            db_test['amount'] = 1

        if col_names.__class__ == str and col_names == ALL:
            col_names = list(db_teach)
        factor_list = self.get_list_factors(col_names)

        compare_diff = []

        for f in factor_list:
            st_teach = Statistic.get_stat_summarise_by_column(db_teach, f)
            st_test = Statistic.get_stat_summarise_by_column(db_test, f)
            st = st_test.merge(st_teach, left_index=True, right_index=True, how='left')
            st.p_y = st.p_y.fillna(0.5)
            diff_val = ((st.p_x - st.p_y) * st.n_x).abs().sum()
            compare_diff.append(diff_val)

        data = {'factor': factor_list, 'compare_diff': compare_diff}
        df = pd.DataFrame(data)
        df.sort_values(by='compare_diff', ascending=False, inplace=True)
        return df

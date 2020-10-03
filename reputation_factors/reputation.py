import numpy as np
import pandas as pd


class Reputation:

    def __init__(self, dt: pd.DataFrame, trusted_days=45, id='id'):
        '''
        self.status -  are {0,1}
        self.date_only - str , example  2018-12-02
        date_second - time in seconds, int
        cb_date_second - time cb in seconds, int
        if status is bad and the field date_cb_only is empty or None, then cb_date_second is negative int
        for   example -9223372037
        '''
        #TODO add amount
        col_names = [id, 'date', 'date_cb_only', 'status']
        df = dt[col_names].copy()
        if id != 'id':
            df = df.rename(columns={id: "id"})

        df['date_only'] = df.date.str[:10]

        df['date_second'] = pd.to_datetime(df.date)
        df.date_second = df.date_second.astype(np.int64) // 10 ** 9

        # TODO cb_date_second  -> date_cb_second
        # TODO cb_date_seconds -> date_cb_seconds
        #

        df['cb_date_second'] = pd.to_datetime(df.date_cb_only)
        df.cb_date_second = df.cb_date_second.astype(np.int64) // 10 ** 9

        df['line_num'] = range(df.shape[0])

        BAD_STATUSES = (1, '1', 'true')
        df.loc[:, 'status'] = np.where(df.status.isin(BAD_STATUSES), 1, 0)

        df = df.sort_values(by=['id', 'date'])

        self.df = df

        self.line_nums = df.line_num.values
        self.ids = df.id.values
       # TODO add amount
       # self.amount = df.amoount.values
        self.statuses = df.status.values

        self.date_only = df.date_only.values

        self.date_seconds = df.date_second.values
        self.cb_date_seconds = df.cb_date_second.values

        self.trusted_days = trusted_days
        self.one_hour_seconds = 60 * 60
        self.one_day_seconds = 24 * self.one_hour_seconds
        self.trusted_seconds = trusted_days * self.one_day_seconds

    def get_current_data(self, line_num):
        return self.date_seconds[line_num], self.cb_date_seconds[line_num], self.date_only[line_num], self.date_seconds[line_num - 1]

    def get_data_by_line_num(self, line_num):
        return self.date_seconds[line_num], self.cb_date_seconds[line_num], self.date_only[line_num], self.statuses[line_num]

    def clear_factors_data(self):
        self.n_previouses = []
        self.n_greys = []
        self.n_bads = []
        self.is_quickes = []
        self.is_first = []
        self.n_in_days = []

    def add_values(self, n_previous, n_grey, n_bad, is_quick, is_first, n_in_day):
        self.n_previouses.append(n_previous)
        self.n_greys.append(n_grey)
        self.n_bads.append(n_bad)
        self.is_quickes.append(is_quick)
        self.is_first.append(is_first)
        self.n_in_days.append(n_in_day)

    def get_factor_as_df(self):
        data = {'line_num': self.line_nums,
                'n_previous': self.n_previouses,
                'n_grey': self.n_greys,
                'n_bad': self.n_bads,
                'is_quick': self.is_quickes,
                'is_first': self.is_first,
                'n_in_day': self.n_in_days
                }
        df = pd.DataFrame(data).sort_values(by='line_num')
        return df

    def create_factors_by_id(self, n_start_id, n_end_id):

        status_good = 0
        status_bad = 1
        trusted_seconds = self.trusted_seconds
        one_hour_seconds = self.one_hour_seconds

        for i in range(n_end_id - n_start_id + 1):
            n_grey = 0
            n_bad = 0
            n_in_day = 0
            n_previous = i
            if i == 0:
                is_first = 1
                is_quick = 0
            else:
                n_current_line = i + n_start_id

                current_date_sec, current_cb_date_sec, current_date_only, previous_date_sec = self.get_current_data(n_current_line)

                is_first = 0
                is_quick = 1 if current_date_sec - previous_date_sec < one_hour_seconds else 0

                for k in range(i):
                    line_num = k + n_start_id

                    date_sec, cb_date_sec, date_only, status = self.get_data_by_line_num(line_num)

                    if status == status_bad and cb_date_sec < current_date_sec:
                        n_bad += 1

                    if current_date_sec - date_sec > trusted_seconds and (
                            status == status_good or cb_date_sec < current_date_sec):
                        n_grey += 1

                    if date_only == current_date_only:
                        n_in_day += 1

            self.add_values(n_previous, n_grey, n_bad, is_quick, is_first, n_in_day)
            #print('n_previous={}, n_grey={}, n_bad={}, is_quick={}, is_first={}'.format(i, n_grey, n_bad, is_quick,  is_first))
        return

    def create_reputation_factors(self):
        self.clear_factors_data()
        ids = self.ids
        n = len(ids)
        n_start_id = 0
        current_id = ids[0]

        for i in range(n):
            if ids[i] != current_id:
                n_end_id = i - 1
                self.create_factors_by_id(n_start_id, n_end_id)
                current_id = ids[i]
                n_start_id = i

            if i == n - 1:
                n_end_id = i
                self.create_factors_by_id(n_start_id, n_end_id)

        return self.get_factor_as_df()
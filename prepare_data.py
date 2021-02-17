COL_FACTORS = ['bin', 'amount', 'bank_currency', 'hour', 'day_of_week', 'longitude', 'latitude', 'phone_2_norm', 'is_gender_undefined', 'is_city_resolved']
COL_FACTORS = sorted(COL_FACTORS)

# For Xgboost
from helper import DataHelper
datahelper = DataHelper(db_teach, db_test, COL_FACTORS)
datahelper.create_train_test()
datahelper.show_columns_with_na()
mean_values = datahelper.get_mean_value()
replaced_values = { col: mean_values[col] for col in ('latitude', 'longitude')}
replaced_values['default'] =  -999
datahelper.replaced_na_values(replaced_values)   
train , test = datahelper.get_train_test()
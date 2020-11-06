import unittest

from tests.data_for_tests import DataForTests
from bayes.naive_bayes import Bayes

class TestNaiveBayes(unittest.TestCase):
    def setUp(self):
        self.db_teach = DataForTests.db_teach
        self.db_test_for_bayes = DataForTests.db_test_for_bayes
        self.feature_imp = DataForTests.feature_imp
        self.compare_res = DataForTests.compare_res
        self.bayes = Bayes()

    def test_get_feature_importance(self):
        result = self.bayes.get_feature_importance(self.db_teach)
        result = result.to_dict()
        expected = self.feature_imp
        self.assertDictEqual(result, expected, 'incorrect data')

    def test_compare_factor_teach_test(self):
        result = self.bayes.compare_factor_teach_test(self.db_teach, self.db_test_for_bayes)
        result = result.to_dict()
        expected = self.compare_res
        self.assertDictEqual(result, expected, 'incorrect data')

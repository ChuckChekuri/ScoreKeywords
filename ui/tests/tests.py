'''Ui tests module'''
# Optionally, you can define a test suite to run all tests
import unittest
from . import test_consumers
from . import test_models
from . import test_views


def suite():
    '''Test suite to run all tests'''
    test_suite = unittest.TestSuite()
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_consumers))
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_models))
    test_suite.addTests(unittest.TestLoader().loadTestsFromModule(test_views))
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())

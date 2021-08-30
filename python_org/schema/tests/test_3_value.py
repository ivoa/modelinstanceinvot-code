'''
Created on 16 juin 2020

@author: laurentmichel
'''
import os, sys, unittest
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)
from schema.tests import logger

from schema.validator.test_runner import TestRunner

mapping_sample = "./mapping_sample"
 

class Test(unittest.TestCase):

    def testOK(self):
        self.assertTrue(TestRunner.testOK(mapping_sample, "test_3"), "file should be valid")

    def testKO(self):
        self.assertTrue(TestRunner.testKO(mapping_sample, "test_3"), "file shouldn't be valid")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

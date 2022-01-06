"""
Created on Feb 26, 2021

@author: laurentmichel
"""
import unittest
import os

from astropy.io.votable import parse

class TestVOTablePointer(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.7.xml")
        votable = parse(vpath)
        votable.resources


    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
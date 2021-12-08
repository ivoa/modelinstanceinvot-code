'''
Created on 8 Dec 2021

@author: laurentmichel
'''
import os
from unittest import TestCase
from utils.dict_utils import DictUtils

class Checker():
    data_path = os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def check_dict(dictionary, ref_file):
        testcase = TestCase()
        testcase.maxDiff = None
        reference = DictUtils.read_dict_from_file(os.path.join(Checker.data_path, "./data/references/", ref_file))
        testcase.assertDictEqual(dictionary, reference)
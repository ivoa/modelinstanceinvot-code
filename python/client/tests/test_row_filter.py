"""
Created on 1 sept. 2021

@author: michel
"""
import os
import unittest

from client.objectbuilder.votable_pointer import  VOTablePointer
from client.objectbuilder.row_filter import RowFilter

class Test(unittest.TestCase):
    def testName(self):
        
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.sample_path = os.path.join(self.data_path, "./data/references/test_table_iterator.input.1.json")
        VOTablePointer.connect(os.path.join(self.data_path, "./data/rich_instance.xml"))

        
        row_filter = RowFilter("test")
        
        # no filtering value
        row_filter.set_filtered_column_number(1)
        data_table = VOTablePointer.get_table("Spectra").to_table()
        row_iter = iter(data_table)
        result = []
        try:
            while True:
                row = next(row_iter)
                if row_filter.row_match(row):
                    result.append([row[0], row[1]])
        except:
            self.assertListEqual(result, [['Spectrum 11', 1], ['Spectrum 12', 1], ['Spectrum 21', 2], ['Spectrum 22', 2]])

        # filter on value 1
        row_filter.set_filtering_value(1)
        row_iter = iter(data_table)
        result = []
        try:
            while True:
                row = next(row_iter)
                if row_filter.row_match(row):
                    result.append([row[0], row[1]])
        except:
            self.assertListEqual(result, [['Spectrum 11', 1], ['Spectrum 12', 1]])

        # filter on value 2
        row_filter.set_filtering_value(2)
        row_iter = iter(data_table)
        result = []
        try:
            while True:
                row = next(row_iter)
                if row_filter.row_match(row):
                    result.append([row[0], row[1]])
        except:
            self.assertListEqual(result, [['Spectrum 21', 2], ['Spectrum 22', 2]])
            
        # filter on value out of range
        row_filter.set_filtering_value(20)
        row_iter = iter(data_table)
        result = []
        try:
            while True:
                row = next(row_iter)
                if row_filter.row_match(row):
                    result.append([row[0], row[1]])
        except:
            self.assertListEqual(result, [])
            
        # filter on the wrong column
        row_filter.set_filtered_column_number(0)
        row_filter.set_filtering_value(1)
        data_table = VOTablePointer.get_table("Spectra").to_table()
        row_iter = iter(data_table)
        result = []
        try:
            while True:
                row = next(row_iter)

                if row_filter.row_match(row):
                    result.append(row)
        except:
            self.assertListEqual(result, [])
        
        
 
if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

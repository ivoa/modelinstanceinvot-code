'''
Created on 30 juin 2020

@author: laurentmichel
'''
import unittest
import os
import sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from astropy.io.votable import parse
from client.inst_builder.join_iterator import JoinIterator


class Test(unittest.TestCase):

    def testName(self):
        self.assertEqual(self.join_iterator.table_mapper.get_flatten_data_head()
                         , ['test:detection(test:detection.id) [col#1 _foreign]', 'test:detection(test:detection.num) [col#0 _num_148]'], "")
        
    def testIter_11(self):
        self.join_iterator.table_mapper.rewind()
        self.join_iterator.set_foreignkey_value(1)
        cpt = 1;
        while True:
            inst = self.join_iterator.table_mapper._get_next_row_instance()
            if inst != None:
                self.assertDictEqual(
                    inst,
                    {
                      "@dmtype": "test:Detection",
                      "test:detection.id": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_foreign",
                        "@value": 1
                      },
                      "test:detection.num": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_num_148",
                        "@value": (10 + cpt)
                      }
                    },
                   "")
                cpt += 1
            else:
                break
            
    def testIter_12(self):
        self.join_iterator.table_mapper.rewind()
        self.join_iterator.set_foreignkey_value(1)
        cpt = 1;
        while True:
            inst = self.join_iterator.table_mapper._get_next_flatten_row()
            if inst != None:
                self.assertListEqual(
                    inst,
                    [1, (10 + cpt)],
                   "")
                cpt += 1
            else:
                break

    def testIter_2(self):
        self.join_iterator.table_mapper.rewind()
        self.join_iterator.set_foreignkey_value(2)
        cpt = 1;
        while True:
            inst = self.join_iterator.table_mapper._get_next_row_instance()
            if inst != None:
                self.assertDictEqual(
                    inst,
                    {
                      "@dmtype": "test:Detection",
                      "test:detection.id": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_foreign",
                        "@value": 2
                      },
                      "test:detection.num": {
                        "@dmtype": "ivoa:real",
                        "@ref": "_num_148",
                        "@value": (20 + cpt)
                      }
                    },
                    "")
                cpt += 1
            else:
                break
            
    def testIter_22(self):
        self.join_iterator.table_mapper.rewind()
        self.join_iterator.set_foreignkey_value(2)
        cpt = 1;
        while True:
            inst = self.join_iterator.table_mapper._get_next_flatten_row()
            if inst != None:
                self.assertListEqual(
                    inst,
                    [2, (20 + cpt)],
                   "")
                cpt += 1
            else:
                break
                                              
    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_joint_instances.xml")
        votable = parse(self.votable_path)
        for table in votable.iter_tables():
            if  "OtherResults" == table.name:
                self.parsed_table = table
                self.join_iterator = JoinIterator(
                    "OtherResults",
                    "_poserr_148",
                    "_foreign",
                    {
                        "@foreign": "_foreign",
                        "@primary": "_poserr_148",
                        "@tableref": "OtherResults",
                        "test:detection": {
                            "@dmtype": "test:Detection",
                            "test:detection.id": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_foreign",
                                "@value": ""
                                },
                            "test:detection.num": {
                                "@dmtype": "ivoa:real",
                                "@ref": "_num_148",
                                "@value": ""
                                }
                            }
                        }
                    )
                self.join_iterator.connect_votable(self.parsed_table)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

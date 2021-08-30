'''
Created on 22 juin 2020

@author: laurentmichel
'''
import unittest
import os
import sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)
from client.inst_builder.vodml_instance import VodmlInstance
from client.tests import logger
from utils.dict_utils import DictUtils


class TestVodmlInstance(unittest.TestCase):
    
    def test_1(self):
        self.maxDiff = None        
        # print(DictUtils.get_pretty_json(self.vodml_instance.json_view))
        self.assertDictEqual(self.vodml_instance.json_view
                             , DictUtils.read_dict_from_file(self.json_ref_path)
                             , "=======")
        
    def test_2(self):
        # print(vodml_instance.table_mappers.keys())
        self.assertListEqual(list(self.vodml_instance.table_mappers.keys()),
                             ['Results', 'OtherResults'],
                             "TableMapper keys not matching")
        
    def test_3(self):
        if self.populated is False:
            self.vodml_instance.populate_templates()
            self.vodml_instance.connect_join_iterators()
            self.populated = True
        self.assertEqual(self.vodml_instance.table_mappers["Results"].join_iterators["OtherResults"].__repr__(),
                             "Join iterator f_table=OtherResults p_key=_poserr_148, f_key=_foreign",
                             "")
    
    def test_4(self):
        if self.populated is False:
            self.vodml_instance.populate_templates()
            self.vodml_instance.connect_join_iterators()
            self.populated = True
        column_mapping = self.vodml_instance.table_mappers["Results"].table_iterators['primary:point'].column_mapping
        self.assertListEqual(list(column_mapping.column_refs.keys()), ['_poserr_148'], "")
    
    def test_21(self):
        self.json_ref_path = os.path.join(self.data_path, "./data/test_vodml_instance_21.json")
        if self.populated is False:
            self.vodml_instance.populate_templates()
            self.vodml_instance.connect_join_iterators()
            self.populated = True
        table_mapper = self.vodml_instance.table_mappers["OtherResults"]
        full_dict = table_mapper.get_full_instance()

        # print(DictUtils.get_pretty_json(full_dict))
        self.assertDictEqual(full_dict, DictUtils.read_dict_from_file(self.json_ref_path), "")
    
    def test_22(self):
        self.json_ref_path = os.path.join(self.data_path, "./data/test_vodml_instance_22.json")
        if self.populated is False:
            self.vodml_instance.populate_templates()
            self.vodml_instance.connect_join_iterators()
            self.populated = True
        table_mapper = self.vodml_instance.table_mappers["Results"]
        full_dict = table_mapper.get_full_instance()

        # print(DictUtils.get_pretty_json(full_dict))
        self.assertDictEqual(full_dict, DictUtils.read_dict_from_file(self.json_ref_path), "")

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_vodml_instance.xml")
        self.json_ref_path = os.path.join(self.data_path, "./data/test_vodml_instance_1.json")

        logger.info("processing %s", self.votable_path)
        self.populated = False
        self.vodml_instance = VodmlInstance(self.votable_path)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

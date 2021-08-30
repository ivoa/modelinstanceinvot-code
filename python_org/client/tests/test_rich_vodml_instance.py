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

    def test_22(self):
        if self.populated is False:
            self.vodml_instance.populate_templates()
            self.vodml_instance.connect_join_iterators()
            self.populated = True
        table_mapper = self.vodml_instance.table_mappers["Results"]
        full_dict = table_mapper.get_full_instance()

        #
        # print(DictUtils.get_pretty_json(full_dict))
        self.assertDictEqual(full_dict, DictUtils.read_dict_from_file(self.json_ref_path), "")

    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_rich_vodml_instance.xml")
        self.json_ref_path = os.path.join(self.data_path, "./data/test_rich_vodml_instance.json")

        logger.info("processing %s", self.votable_path)
        self.populated = False
        self.vodml_instance = VodmlInstance(self.votable_path)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

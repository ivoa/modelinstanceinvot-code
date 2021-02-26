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
from client.inst_builder.vodml_instance import VodmlInstance
from utils.dict_utils import DictUtils

from client.tests import logger


class Test(unittest.TestCase):

    def test_1(self):
        self.json_ref_path = os.path.join(self.data_path, "./data/test_vodml_instance_21.json")
        if self.populated is False:
            self.vodml_instance.populate_templates()
            self.vodml_instance.connect_join_iterators()
            self.populated = True
        table_mapper = self.vodml_instance.table_mappers["Results"]
        full_dict = table_mapper.get_full_instance()
        # print(DictUtils.get_pretty_json(full_dict))
                                              
    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/test_joint_instances.xml")
        self.json_ref_path = os.path.join(self.data_path, "./data/test_vodml_instance_1.json")

        logger.info("processing %s", self.votable_path)
        self.populated = False
        self.vodml_instance = VodmlInstance(self.votable_path)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

"""
Created on 1 sept. 2021

@author: michel
"""
import os
import unittest
from utils.dict_utils import DictUtils
from client.objectbuilder.vodml_instance import VodmlInstance


class Test(unittest.TestCase):
    def testName(self):
        self.maxDiff = None
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.json_path = os.path.join(self.data_path, "./data/rich_instance.xml")
        vodml_instance = VodmlInstance(self.json_path)

        self.assertListEqual(
            list(vodml_instance.table_mappers.keys()),
            ["Results", "OtherResults", "Spectra"],
        )

        # DictUtils.print_pretty_json(vodml_instance.table_mappers["Results"].json)
        vodml_instance.get_root_element("test.model")
        self.assertDictEqual(
            vodml_instance.json_view,
            DictUtils.read_dict_from_file( 
                os.path.join(self.data_path, "./data/references/vodml_instance.1.json")
                )
            )
 


        model_instance = vodml_instance.get_instance()
        self.assertDictEqual(
            model_instance,
             DictUtils.read_dict_from_file( 
                os.path.join(self.data_path, "./data/references/vodml_instance.2.json")
                )

        )


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

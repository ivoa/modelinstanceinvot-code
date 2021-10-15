'''
Created on 1 sept. 2021

@author: michel
'''
import os
import unittest
from client.objectbuilder.vodml_instance import VodmlInstance
from client.objectbuilder.table_mapper import TableMapper
from astropy.io.votable import parse
from utils.dict_utils import DictUtils


class Test(unittest.TestCase):


    def testName(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))
        self.votable_path = os.path.join(self.data_path, "./data/rich_instance.xml")
        votable = parse(self.votable_path)
        vodml_instance = VodmlInstance(self.votable_path)

        for resource in votable.resources:
            for table in resource.tables:
                parsed_table = table
                break 
            
        table_mapper = TableMapper(table.name, self.votable_path, json_inst_dict=vodml_instance.json_view)
        table_mapper.map_columns()
        DictUtils.print_pretty_json(table_mapper.table_json)
        print(table_mapper.column_mapping)
        table_mapper.resolve_refs_and_values()
        print(table_mapper.column_mapping)
        print(table_mapper.join_iterators)





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
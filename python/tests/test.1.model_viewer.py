"""
Created on Jan 6, 2022

@author: laurentmichel
"""
import unittest
import os
from astropy.io.votable import parse

from utils.xml_utils import XmlUtils
from utils.dict_utils import DictUtils
from client.xml_interpreter.model_viewer import ModelViewer

class TestModelViewer(unittest.TestCase):
    votable = None
    mviewer = None
    def test_global_getters(self):      
        self.maxDiff = None
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['_PKTable', 'Results'])
        self.assertDictEqual(self.mviewer.get_globals_models(), 
                             DictUtils.read_dict_from_file(os.path.join(
                                 self.data_path, "data/output/test.1.11.json")))
        DictUtils.print_pretty_json(self.mviewer.get_globals_models())
        DictUtils.print_pretty_json(self.mviewer.get_templates_models())
        self.assertDictEqual(self.mviewer.get_templates_models(), 
                             DictUtils.read_dict_from_file(os.path.join(
                                 self.data_path, "data/output/test.1.12.json")))
          
        self.mviewer.connect_table('_PKTable')
        row = self.mviewer.get_next_row()       
        self.assertEqual(row[0], '5813181197970338560')
        self.assertEqual(row[1], 'G')
        
        row = self.mviewer.get_next_row()
        self.assertEqual(row[0], '5813181197970338560')
        self.assertEqual(row[1], 'BP')

        self.mviewer.rewind()
        row = self.mviewer.get_next_row()       
        self.assertEqual(row[0], '5813181197970338560')
        self.assertEqual(row[1], 'G')

        XmlUtils.assertXmltreeEqualsFile(self.mviewer._templates,
                                       os.path.join(self.data_path, "data/output/test.1.3.xml"))
        XmlUtils.assertXmltreeEqualsFile(self.mviewer._dyn_references["REFERENCE_2"],
                                       os.path.join(self.data_path, "data/output/test.1.4.xml"))
        XmlUtils.assertXmltreeEqualsFile(self.mviewer._joins["JOIN_6"],
                                       os.path.join(self.data_path, "data/output/test.1.5.xml"))
        model_view = self.mviewer.get_model_view()
        XmlUtils.pretty_print(model_view)
        
        # We stop here meanwhile we decide how to handle join data
        import sys
        sys.exit(1)
        
        XmlUtils.assertXmltreeEqualsFile(model_view,
                                       os.path.join(self.data_path, "data/output/test.1.8.xml"))
    
        json_view = self.mviewer.get_model_view()
        self.assertListEqual(
            json_view,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.1.9.json"
                )
            ),
        )

        self.assertListEqual(
            self.mviewer.get_json_model_component_by_type("ds:experiment.ObsDataset"),
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.1.10.json"
                )
            ),
        )
        
        self.assertListEqual(
            self.mviewer.get_json_model_component_by_role("ds:experiment.ObsDataset.target"),
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.1.13.json"
                )
            ),
        )

        
        
        self.mviewer.connect_table('Results')
        
        XmlUtils.assertXmltreeEqualsFile(self.mviewer._templates,
                                       os.path.join(self.data_path, "data/output/test.1.6.xml"))
        self.mviewer.get_next_row()
        model_view = self.mviewer.get_model_view()    
        XmlUtils.assertXmltreeEqualsFile(model_view,
                                       os.path.join(self.data_path, "data/output/test.1.7.xml"))
        json_view = self.mviewer.get_json_model_view()
        self.assertListEqual(
            json_view,
            DictUtils.read_dict_from_file(
                os.path.join(
                    self.data_path, "data/output/test.1.8.json"
                )
            ),
        )


    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/input/test.1.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "data/input/test.1.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
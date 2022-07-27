"""
Created on July 27, 2022

This test show up how to retrieve data from a mapping block.

The purpose of the test is to show that data and meta-data can be retrieved
by only accessing the mapping blocks. 
All VOTable access are operated by the model viewer behind the stage

- works with test.14.xml, a GAIA time series mapped on the 
  prototype of the SpaseCUbe model.
  
- There is not specific Python class to hold SparseCubes. 
  The code below just picks mode components.
  
- The mapping is done on models as they was in 2021. 
  The purpose if the tool is to validate the mapping processing not the models.
    
- The following operations have been implemented
  - Extraction of the mapping block applied to the first row
    - tested against a reference file
  - JSON serialization of the mapping block applied to the first row
    - tested against a reference file
  - Extraction of the XML serialization of the DataSet instance
    - tested against a reference file
  - Extraction of the photometric points by using the VO-Model place-holder classes
    - The used MC classes do include the modification required by the RFC  in 2022 
    - tested against a reference file
     
@author: laurentmichel
"""
import unittest
import os
from astropy.io.votable import parse

from mivot_code.utils.xml_utils import XmlUtils
from mivot_code.utils.dict_utils import DictUtils
from mivot_code.client.xml_interpreter.model_viewer import ModelViewer

class TestModelViewer(unittest.TestCase):
    votable = None
    mviewer = None
    def test_global_getters(self):      
        self.maxDiff = None
        # Checks that the VOTable has the expected TABLEs
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['_PKTable', 'Results'])
        
        # Connect the head table
        # This operation will be automated in a production code
        self.mviewer.connect_table('_PKTable')
        self.mviewer.get_next_row()  
        
        # Extract the SparseCube instance
        sparse_cubes = self.mviewer.get_model_component_by_type("cube:SparseCube")  
        # make sure we got only one      
        self.assertEqual(len(sparse_cubes), 1)
        # take that one      
        sparse_cube = sparse_cubes[0]    
        # And valid its XML serialization against  a reference file   
        XmlUtils.assertXmltreeEqualsFile(sparse_cube,
                                         os.path.join(self.data_path, "data/output/test.14.sparsecube.xml"))
        # And valid its JSON serialization against  a reference file   
        json_cube_view = self.mviewer.get_json_model_view()[0]
        self.assertDictEqual(json_cube_view,
                             DictUtils.read_dict_from_file(os.path.join(self.data_path, "data/output/test.14.sparsecube.json")))

        # extract the DataSet instance
        datasets = self.mviewer.get_model_component_by_role("cube:DataProduct.dataset")
        # make sure we got only one      
        self.assertEqual(len(datasets), 1)
        # take that one      
        dataset = datasets[0]        
        # And valid it XML serialization against  a reference file   
        XmlUtils.assertXmltreeEqualsFile(dataset,
                                         os.path.join(self.data_path, "data/output/test.14.dataset.xml"))

        
        # extract the DataSet instance
        phot_header = ["Time (d)", None, None]
        phot_points = []
        # Get first all time stamps
        times = self.mviewer.get_stc_times()
        for single_time in times:
            phot_points.append([single_time.coord.date, None, None])

        phot_values = self.mviewer.get_stc_generic_measures()
        indx = 0
        # Get then all magnitudes
        for phot_value in phot_values:
            if phot_value.coord.cval.unit == "mag":
                phot_points[indx][1] = phot_value.coord.cval.value
                phot_header[1] = f"Magnitude ({phot_value.coord.cval.unit})"
                indx += 1
        indx = 0
        # Get then all fluxes
        for phot_value in phot_values:
            if phot_value.coord.cval.unit != "mag":
                phot_header[2] = f"Flux ({phot_value.coord.cval.unit})"
                phot_points[indx][2] = phot_value.coord.cval.value
                indx += 1
        # Package  all in a JSON
        ndpoints = {"header": phot_header, "data": phot_points}
        self.assertEqual(len(ndpoints["data"]), 85)

        self.assertDictEqual(ndpoints,
                             DictUtils.read_dict_from_file(os.path.join(self.data_path, "data/output/test.14.data.json")))

    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/input/test.14.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "data/input/test.14.xml"))
            break;


if __name__ == "__main__":
    unittest.main()
"""
Created on Jan 6, 2022

@author: laurentmichel
"""
import unittest
import os
import logging
import matplotlib
import mplcursors
import matplotlib.pyplot as plt 

import numpy as np
from astropy.io.votable import parse
from utils.quantity_converter import QuantityConverter
from client.xml_interpreter.model_viewer import ModelViewer

matplotlib.font_manager: logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
class TestLonLatPoint(unittest.TestCase):
    votable = None
    mviewer = None
    def test_global_getters(self):      
        self.maxDiff = None
        self.assertListEqual(self.mviewer.get_table_ids(),
                             ['Results'])
        self.mviewer.connect_table('Results')
        times = []
        ras = []
        decs = []
        dist = []       
        must_convert = False
        first_row = True
        while True:
            row = self.mviewer.get_next_row() 
            if row is None:
                break  
            
            position = self.mviewer.get_stc_positions()[0]

            if first_row is True:
                first_row = False
                if position.coord.dist.unit == "parsec":
                    must_convert = True
                    
            if must_convert is True:       
                position.coord.dist.value = QuantityConverter.parallax_to_distance(position.coord.dist.value)
                position.error.plus[2].value = QuantityConverter.parallax_to_distance(position.error.plus[2].value)
                position.error.minus[2].value = QuantityConverter.parallax_to_distance(position.error.minus[2].value)
            
            if not np.isnan(position.coord.dist.value) and position.coord.dist.value < 5000.0:
                ras.append(position.coord.lon.value)    
                decs.append(position.coord.lat.value)   
                dist.append(position.coord.dist.value)   
                pm = self.mviewer.get_stc_measures_by_ucd("pos.pm")[0]
                times.append(f"Proper Motion ({pm.coord.lon.unit}):\nra:{pm.coord.lon.value:.2f} \ndec:{pm.coord.lat.value:.2f}")

            
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(ras, decs, dist)
        ax.set_xlabel('RA')
        ax.set_ylabel('DEC')
        ax.set_zlabel('Dist (parsec)')
        mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(times[sel.index]))
        plt.show()
   
    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/annotated_data/")
        cls.votable = parse(os.path.join(cls.data_path, "gaia_luhman16.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "gaia_luhman16.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
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
        while True:
            row = self.mviewer.get_next_row() 
            if row is None:
                break  
            
            position = self.mviewer.get_stc_positions()[0]
            ras.append(position.coord.lon.value)    
            decs.append(position.coord.lat.value)   
            
            hr = self.mviewer.get_stc_generic_measures()

            times.append(f"Obs time: {self.mviewer.get_stc_times()[0].coord.datetime}"\
                        f"\nra:{position.coord.lon.value}"\
                        f"\ndec: {position.coord.lat.value}"
                        f"\nhr1: {hr[0].coord.cval} +/- {hr[0].error.radius}"\
                        f"\nhr2: {hr[1].coord.cval} +/- {hr[1].error.radius}"\
                        f"\nhr3: {hr[2].coord.cval} +/- {hr[2].error.radius}"\
                        f"\nhr4: {hr[3].coord.cval} +/- {hr[3].error.radius}"
                        ) 
        ram = 0.0
        for ra in ras:
            ram += ra
        ram /= len(ras)
        decm = 0.0
        for dec in decs:
            decm += dec
        decm /= len(decs)
        
        for i in range(len(ras)):
            ras[i] = 3600*(ras[i] - ram)
            decs[i] = 3600*(decs[i] - decm)
        np.random.seed(42)
        
        plt.scatter(ras, decs)
        plt.title("4XMM J174544.4-290024 over 20 years")
        plt.xlabel("delta RA arcsec")
        plt.ylabel("delta DEC arcsec")
        mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(times[sel.index]))
        
        plt.show()
 
    @classmethod
    def setUpClass(cls):
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/xmm_move_hr.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "data/xmm_move_hr.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
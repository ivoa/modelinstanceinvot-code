"""

## Meas/Coords Validation

This goal of this example is to show that real data can be mapped on Measure classes and that the Measure object quantities can be retrieved by generice code.

We proceed with data mapped on individual Measure objects in order to avoid bias possibly introduced by some host model.

This workflow validates the [Measure](https://github.com/ivoa/modelinstanceinvot-code) model (and its coordinates(https://github.com/ivoa-std/CoordinateDM)) in the extand of the the implemented classes.


### Test Case

The VOtable has been queried from tme ESAC archive (https://gea.esac.esa.int/tap-server/tap) with the following query:
```
SELECT TOP 100 gaiadr2.gaia_source.designation , gaiadr2.gaia_source.ra , gaiadr2.gaia_source.ra_error , gaiadr2.gaia_source.\"dec\" , gaiadr2.gaia_source.dec_error , gaiadr2.gaia_source.parallax , gaiadr2.gaia_source.parallax_error , gaiadr2.gaia_source.pmra , gaiadr2.gaia_source.pmra_error , gaiadr2.gaia_source.pmdec , gaiadr2.gaia_source.pmdec_error
 FROM  gaiadr2.gaia_source
 WHERE ( CONTAINS(POINT('ICRS', ra, \"dec\"), CIRCLE('ICRS', 162.328814, -53.319466, 0.016666666666666666)) = 1 )
```

We select positions, parallax and proper motions around `luhman 16`. 

The test goal is to validate the 3D position. To get that third dimension, we map the Gaia parallax on `Position.dist`. This way to proceed requires to client ot be able to detect this pattern and to transform the parallax into a distance.

There is currently no standard method to handle this sort of implicit transformation. We are doing it here just because we know it is part the test.

This opens the issue of defining a client behaviour when the <FIELD> unit does not match the <ATTRIBUTE> unit.

    
- We are using the annotation [syntax](https://github.com/ivoa-std/ModelInstanceInVot) that has been designed after the 2021 workshop.
- The Python code used for this notebook is being [developped](https://github.com/ivoa/modelinstanceinvot-code) to design qnd validate the processing of model annotation.
- This notebook does not pretend to have any scientific value, it is juste a validation case for the mapping syntax \n"

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
from mivot_code.utils.quantity_converter import QuantityConverter

from mivot_code.client.xml_interpreter.model_viewer import ModelViewer

matplotlib.font_manager: logging.getLogger('matplotlib.font_manager').setLevel(logging.WARNING)
class TestLonLatDistPoint(unittest.TestCase):
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
        cls.data_path = os.path.dirname(os.path.realpath(__file__))
        cls.votable = parse(os.path.join(cls.data_path, "data/gaia_luhman16.xml"))
        
        cls.mviewer = None
        for resource in cls.votable.resources:
            cls.mviewer = ModelViewer(resource, votable_path=os.path.join(cls.data_path, "data/gaia_luhman16.xml"))
            break;


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
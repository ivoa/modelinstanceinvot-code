"""
Created on jan  2022

@author: laurentmichel
"""
import unittest
import os

from astropy.io.votable import parse
from mivot_code.client.xml_interpreter.resource_seeker import ResourceSeeker
class TestVResourceSeeker(unittest.TestCase):

    def test_PKTable(self):      
        self.maxDiff = None
        vpath = os.path.join(self.data_path, "data/input/test.7.xml")
        votable = parse(vpath)
        
        rseeker = None
        for resource in votable.resources:
            rseeker = ResourceSeeker(resource)
            break;

        self.assertListEqual(rseeker.get_table_ids(), ['_PKTable', 'Results'])
        
        self.assertDictEqual(rseeker.get_id_index_mapping('_PKTable'), 
                             {'_pksrcid': 0, '_pkband': 1})
        self.assertDictEqual(rseeker.get_id_index_mapping('Results'), 
                             {'_srcid': 0, 'transit_id': 1, '_band': 2, '_obstime': 3, 
                              '_mag': 4, '_flux': 5, '_fluxerr': 6, 'flux_over_error': 7, 
                              'rejected_by_photometry': 8, 'rejected_by_variability': 9, 
                              'other_flags': 10, 'solution_id': 11})


    def setUp(self):
        self.data_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
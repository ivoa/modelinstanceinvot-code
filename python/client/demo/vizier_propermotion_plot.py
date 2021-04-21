'''

Read an annotated VOTABLE and show different outputs
Created on 31 mars 2020

@author: laurentmichel
'''

import os, sys
from client.parser.mango_browser import MangoBrowser

file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from utils.dict_utils import DictUtils

from client.demo import data_dir

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    votable_path = os.path.join(data_dir,
                                "annotated_data",
                                "vizier_propermotion.annot.xml"
      
                               )
    mango_browser = MangoBrowser(votable_path) 
    
    mango_parameters = mango_browser.get_parameters()
    print(DictUtils.get_pretty_json(mango_parameters))

    proper_motions = mango_browser.get_data(measure_type="meas:ProperMotion")
    print(DictUtils.get_pretty_json(proper_motions))
    
    proper_motions = mango_browser.get_data(measure_type="meas:Position")
    print(DictUtils.get_pretty_json(proper_motions))
    
    proper_motions = mango_browser.get_data()
    print(DictUtils.get_pretty_json(proper_motions))



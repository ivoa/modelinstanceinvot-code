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
                                "4xmm_litewithsp.annot.xml"
                                )
    
    mango_browser = MangoBrowser(votable_path) 
    
    mango_parameters = mango_browser.get_parameters()
    print("======== Parameters ")
    DictUtils.print_pretty_json(mango_parameters)
    
    associated_data = mango_browser.get_associated_data()
    print("======== Associated data ")
    DictUtils.print_pretty_json(associated_data)
    
    print("======== 1st row data ")
    mango_data = mango_browser.get_data()
    DictUtils.print_pretty_json(mango_data)
    

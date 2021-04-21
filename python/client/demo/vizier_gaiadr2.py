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
from client.inst_builder.vodml_instance import VodmlInstance

from client.demo import data_dir

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    votable_path = os.path.join(data_dir,
                                "annotated_data",
                                "vizier_gaiadr2.annot.xml"
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

    sys.exit()
    vodml_instance = VodmlInstance(votable_path)
    vodml_instance.populate_templates()
    vodml_instance.connect_join_iterators()

    instance = vodml_instance.get_root_element("mango:MangoObject")
    if instance is None:
        raise Exception("No root element found")
    
    print("=== Mapping of the columns")
    print(instance.get_flatten_data_head())
    # print(instance.get_data_subset_keys())
    print("=== First row: flatten mode")
    while True:
        inst = instance._get_next_flatten_row()
        if inst != None:
            print(DictUtils.get_pretty_json(inst))
            break
        else:
            break

    print("=== Second row: instance mode")
    while True:
        inst = instance._get_next_row_instance()
        if inst != None:
            print(DictUtils.get_pretty_json(inst))
            break
        else:
            break
    

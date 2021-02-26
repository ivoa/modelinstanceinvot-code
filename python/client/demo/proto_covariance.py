'''

Read an annotated VOTABLE and show different outputs
Created on 31 mars 2020

@author: laurentmichel
'''

import os, sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from utils.dict_utils import DictUtils
from client.inst_builder.vodml_instance import VodmlInstance
from client.parser.instance_browser import InstanceBrowser 

from client.demo import data_dir

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    votable_path = os.path.join(data_dir,
                                "annotated_data",
                                "proto_covariance.annot.xml"
                                )
    vodml_instance = VodmlInstance(votable_path)
    vodml_instance.populate_templates()
    vodml_instance.connect_join_iterators()

    instance = vodml_instance.get_root_element("mango:MangoObject")
    if instance is None:
        raise Exception("No root element found")
    
    print("=== Mapping of the columns")
    print(instance.get_flatten_data_head())

    print("=== first row: instance mode")
    inst = None
    while True:
        inst = instance._get_next_row_instance()
        if inst != None:
            print(DictUtils.get_pretty_json(inst))
            break
        else:
            break

    instance_browser = InstanceBrowser(inst)
    print("Source identifier" + DictUtils.get_pretty_json(instance_browser.get_identifier()))
    print(DictUtils.get_pretty_json(instance_browser.get_parameter_list()))
    

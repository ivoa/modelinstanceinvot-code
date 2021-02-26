'''

Read an annotated VOTABLE and show different outputs
Created on 31 mars 2020

@author: laurentmichel
'''

import os, sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from client.demo import data_dir

from utils.dict_utils import DictUtils

from client.inst_builder.vodml_instance import VodmlInstance

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    votable_path = os.path.join(data_dir,
                                "annotated_data",
                                "vizier_votable_avecActivity_Vo-dml-lite.xml"
                                )
    vodml_instance = VodmlInstance(votable_path)
    vodml_instance.populate_templates()
    vodml_instance.connect_join_iterators()

    instance = vodml_instance.get_root_element("voprov:Entity")
    
    print(DictUtils.get_pretty_json(instance.json))
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
    

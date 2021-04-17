'''

Read an annotated VOTABLE and show different outputs
Created on 31 mars 2020

@author: laurentmichel
'''

import os, sys
from utils.dict_utils import DictUtils

file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)

from client.inst_builder.vodml_instance import VodmlInstance

from client.demo import data_dir

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    votable_path = os.path.join(data_dir,
                                "annotated_data",
                                "TimeSeriesMangoZTF.annot.xml"
                                )
    vodml_instance = VodmlInstance(votable_path)
    vodml_instance.populate_templates()
    vodml_instance.connect_join_iterators()
    
    instance = vodml_instance.get_root_element("mango:MangoObject")
    table_mapper = vodml_instance.table_mappers["Results"]

    #print(DictUtils.get_pretty_json(table_mapper.get_datatable_mapping()))
    #sys.exit()
    
    print(instance.json["MODEL_INSTANCE"]["TABLE_MAPPING"]["Results"].keys())
    for k in (k for k in instance.json["MODEL_INSTANCE"]["TABLE_MAPPING"]["Results"].keys() if k.startswith("@") is False):
        #print(DictUtils.get_pretty_json(instance.json["MODEL_INSTANCE"]["TABLE_MAPPING"]["Results"][k]))
        print("================= source " + k)
        print("=== Mapping of the columns")
        print(instance.get_flatten_data_head())

        cpt = 0
        while True:
            inst = instance._get_next_flatten_row(data_subset=("root_" + k))
            if inst != None and cpt < 3:
                print(DictUtils.get_pretty_json(inst))
            else:
                print(".... etc ....")
                break
            cpt += 1
        table_mapper.rewind()


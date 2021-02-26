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

from client.demo import data_dir
from client.inst_builder.astropy_wrapper import AstropyWrapper

if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    votable_path = os.path.join(data_dir,
                                "annotated_data",
                                "4xmm_detections.annot.xml"
                                )
    vodml_instance = VodmlInstance(votable_path)
    vodml_instance.populate_templates(resolve_refs=True)
    vodml_instance.connect_join_iterators()
    table_row_instances = vodml_instance.get_root_element("mango:MangoObject")

    if len(vodml_instance.table_mappers) == 0:
        print("no table mapper")
        sys.exit(1)
    mapper_name = None
    for k, v in vodml_instance.table_mappers.items():
        print("process table mapper {}".format(k))
        mapper_name = k
        break;
    
    while True:
        inst = table_row_instances._get_next_row_instance()
        if inst != None:
            print(DictUtils.get_pretty_json(inst))
        break   

    wrapper = AstropyWrapper(vodml_instance, mapper_name)
    
    print(f"Astropy space frame: {wrapper.get_space_frame(inst)}")
    print(f"Astropy time frame: {wrapper.get_time_frame(inst)}")
    
    '''
    # output
    
    Astropy space frame: <ICRS Frame>
    Astropy time frame: ('tcb', <EarthLocation (0., 0., 0.) m>, 'mjd')
    '''
    

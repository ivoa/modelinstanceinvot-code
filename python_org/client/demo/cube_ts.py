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
                                "cube_ts.annot.xml"
                                )
    vodml_instance = VodmlInstance(votable_path)
    vodml_instance.populate_templates()
    vodml_instance.connect_join_iterators()

    instance = vodml_instance.get_root_element("cube:SparseCube")
    if instance is None:
        raise Exception("No root element found")
    
    instance_browser = InstanceBrowser(instance.json)
    coord_systems = instance_browser.get_globals_types()
    print("=== Coords Systems")
    print(coord_systems)
    
    for coord_system in coord_systems:
        if coord_system.endswith("SpaceSys"):
            print("====== Space Coord System")
            print(DictUtils.get_pretty_json(instance_browser.get_globals_by_type(coord_system)))
        elif coord_system.endswith("TimeSys"):
            print("====== Time Coord System")
            print(DictUtils.get_pretty_json(instance_browser.get_globals_by_type(coord_system)))
        elif coord_system.endswith("PhotometryCoordSys"):
            print("====== Photometry Coord System")
            print(DictUtils.get_pretty_json(instance_browser.get_globals_by_type(coord_system)))
    root_object = instance_browser.get_root_element()
    
    print("=== Roles of the components of the root object")
    root_component_roles = instance_browser.get_root_component_roles()
    print(root_component_roles)
    
    for root_component_role in root_component_roles:
        if root_component_role.endswith("dataset"):
            print("====== Dataset Instance (role={})".format(root_component_role))
            print(DictUtils.get_pretty_json(instance_browser.get_root_component_by_role(root_component_role)))
    
    print("=== Mapping of the columns")
    print(instance.get_flatten_data_head())

    print("=== flatten rows")
    inst = None
    while True:
        inst = instance._get_next_flatten_row()
        if inst != None:
            print(DictUtils.get_pretty_json(inst))
        else:
            break
    
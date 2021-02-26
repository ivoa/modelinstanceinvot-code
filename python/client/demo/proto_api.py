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


def map_measures(votable_path):
    vodml_instance = VodmlInstance(votable_path)
    vodml_instance.populate_templates()
    vodml_instance.connect_join_iterators()

    instance = vodml_instance.get_root_element("mango:MangoObject")
    if instance is None:
        raise Exception("No root element found")
    
    while True:
        inst = instance._get_next_row_instance()
        if inst != None:
            break
        else:
            break

    # BUG 2 parameters arrays are nested
    # TODO 2 be fixed
    parameters = inst["mango:MangoObject.parameters"]
    parameter_map = {}
    for parameter in parameters:
        ucd = parameter["mango:Parameter.ucd"]["@value"]
        classe = parameter["mango:Parameter.measure"]["@dmtype"]
        semantic = parameter["mango:Parameter.semantic"]["@value"]
        description = parameter["mango:Parameter.description"]["@value"]
        parameter_map[classe] = {"class": classe, "ucd": ucd, "semantic": semantic, "description": description}
    return parameter_map


if __name__ == '__main__':
    base_path = os.path.dirname(os.path.realpath(__file__)) 
    for vot in ["vizier_propermotion.annot.xml", "4xmm_detections.annot.xml"]:
        votable_path = os.path.join(data_dir,
                                "annotated_data",
                                vot
                                )
        parameter_map = map_measures(votable_path)
        print(DictUtils.get_pretty_json(parameter_map))
    

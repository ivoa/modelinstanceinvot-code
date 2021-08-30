#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

Generates a CAB-MSD position measurement  mapping block

Created on 15 avr. 2020

@author: laurentmichel
'''

import os, json, sys
file_path = os.path.dirname(os.path.realpath(__file__)) + "/../../"
if file_path not in sys.path:
    sys.path.append(file_path)
from lxml import etree

from mapping_factory.factory.mapping_generator import  MappingGenerator
from mapping_factory.launchers import data_dir

            
def main():
    mapping_generator = MappingGenerator()
    mapping_generator.parse_vodml_file(filename=(data_dir + "/models/STC_meas-v1.0.vo-dml.xml"),
                                       model='meas')
    mapping_generator.resolve_inheritance();
    mapping_generator.resolve_constaints();
    # root_object_id = 'cube:DataProduct'
    mapping_generator.root_object_id = 'meas:ProperMotion'
    # set the concrete object types
    mapping_generator.concrete_classes = {
        "coords:SpaceFrame.refPosition": ["coords:StdRefLocation"],
        "coords:Coordinate.coordSys": ["coords:SpaceSys"],
        "coords:PhysicalCoordSys.frame": ["coords:SpaceFrame"],
        "coords:PhysicalCoordSys.coordSpace": ["coords:SphericalCoordSpace"]
        }
    # set the concrete data types
    mapping_generator.concrete_types = {
        "coords:Point.axis1": "ivoa:RealQuantity",
        "coords:Point.axis2": "ivoa:RealQuantity",
        "coords:Point.axis3": "ivoa:RealQuantity",
        "coords:PhysicalCoordinate.cval": "ivoa:RealQuantity",
        "meas:Error.statError": "meas:Ellipse",
        "meas:Error.sysError": "meas:Ellipse",
        "coords:SpaceFrame.refPosition": "coords:StdRefLocation"
    }
 
    mapping_generator.generate_mapping()
    
    for ac in mapping_generator.mapped_abstract_classes :
        print("Abstract class mapped " + ac)
        for sc in mapping_generator.get_sub_classes(ac):
            abstract = ""
            if  mapping_generator.object_types[sc].abstract == True:
                abstract = "Abstract "
            print("   " + abstract + sc)
            if abstract != "":
                for sc2 in mapping_generator.get_sub_classes(sc):
                    print("       " + sc2)
               
    for ac in mapping_generator.mapped_abstract_types :
        print("Abstract type mapped " + ac)
        for sc in mapping_generator.get_sub_types(ac):
            print("   " + sc)

    root = etree.fromstring(mapping_generator.xml_string + "\n")
    print((etree.tostring(root, pretty_print=True)).decode("utf-8"))


if __name__ == "__main__":
    main()   
    sys.exit()   
        
    

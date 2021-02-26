'''
Created on Oct 15, 2020

@author: laurentmichel
'''
import os
import json

from product_annoter.mapper import logger
from product_annoter.mapper.lonlat_position_appender import LonLatPositionAppender  
from product_annoter.mapper.lonlat_position_ellerr_appender import LonLatPositionEllErrAppender 
from product_annoter.mapper.status_appender import StatusAppender  
from product_annoter.mapper.votable_merger import VOTableMerger
from product_annoter.mapper.identifier_appender import IdentifierAppender
from product_annoter.mapper.photometry_appender import PhotometryAppender
from product_annoter.mapper.genericmeasure_appender  import GenericAppender
from product_annoter.mapper.hardnessratio_appender  import HardnessRatioAppender
from product_annoter.mapper.detectionflag_appender import DetectionFlagAppender
from product_annoter.mapper.mjd_appender import MJDAppender
from product_annoter.mapper.position_appender import PositionAppender
from product_annoter.mapper.propermotion_appender import ProperMotionAppender


class ProductMapper(object):
    '''
    classdocs
    '''

    def __init__(self, data_dir, product_prefix):
        '''
        Constructor
        '''
                # path of the initial VOTable
        self.raw_votable_path = os.path.join(
            data_dir,
            "raw_data",
            product_prefix + ".xml")  
        # path of the annotated VOTable
        self.annot_votable_path = os.path.join(
            data_dir,
            "annotated_data",
            product_prefix + ".annot.xml")
        # Directory with all the mapping components
        self.component_path = os.path.join(
            data_dir,
            "mapping_components")
        # Path of the empty MANGO mapping block
        # This mapping block will host all parameters
        # to be mapped for this VOTable
        self.mango_path = os.path.join(
            self.component_path,
            "mango.mapping.xml")  
        # Output file with just the mapping block
        self.output_mapping_path = os.path.join(
            data_dir,
            "annotated_data",
            product_prefix + ".mapping.xml")
        
        # Read the mapping configuration for this VOTable.
        # This configuration lists a  parameters to be mapped 
        # with the column references or the literal values
        with open(os.path.join(data_dir, 'product_configs', product_prefix + ".mango.config.json")) as json_file:
            self.mapping_config = json.load(json_file)
            
    def build_annotations(self):
        # set the source identifier mapping
        # This is the only mandatory source parameter  
        appender = IdentifierAppender(self.mango_path)
        appender.append_measure(self.mapping_config)
        appender.save(self.output_mapping_path)
    
        # Iterate upon all the parameters to be instanciated
        # The is one appender class for each parameter class
        for measure in self.mapping_config["parameters"]:
            appender = None
           
            if measure["measure"] == "LonLatSkyPositionEllErr":
                logger.info("Position found")
                # FAIT 
                appender = LonLatPositionEllErrAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "LonLatSkyPosition":
                logger.info("Position found")
                # FAIT 
                appender = LonLatPositionAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "Position":
                logger.info("Status found")
                # FAIT 
                appender = PositionAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "ProperMotion":
                logger.info("Status found")
                # FAIT 
                appender = ProperMotionAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "status":
                logger.info("Status found")
                # appender = StatusAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "Photometry":
                logger.info("Photometry found")
                # FAIT 
                appender = PhotometryAppender(self.output_mapping_path, self.component_path)               
            elif measure["measure"] == "GenericMeasure":
                logger.info("GenericMeasure found")
                # FAIT 
                appender = GenericAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "HardnessRatio":
                logger.info("GenericMeasure found")
                # FAIT
                appender = HardnessRatioAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "DetectionFlag":
                logger.info("DetectionFlag found")
                # FAIT
                appender = DetectionFlagAppender(self.output_mapping_path, self.component_path)
            elif measure["measure"] == "MJD":
                logger.info("MJD found")
                appender = MJDAppender(self.output_mapping_path, self.component_path)
               
            if appender is not None:
                # Build the mapping block for the current measure
                appender.append_measure(measure)
                # Save the file with just the mapping block
                appender.save(self.output_mapping_path)
    
        # Insert the mapping block in the head of the VOTable
        merger = VOTableMerger(self.raw_votable_path, self.output_mapping_path, self.annot_votable_path)
        merger.insert_mapping()
            
        

'''
Created on 17 juin 2020

@author: laurentmichel
'''
import os
from schema.validator import logger, data_dir, project_dir
from schema.validator.validator import Validator


class TestRunner:
    validator = Validator(os.path.join(project_dir
                                   , "schema"
                                   , "model-instance-in-vot.xsd"))
    
    @staticmethod
    def testOK(mapping_sample, case_prefix):
        files = os.listdir(mapping_sample)
        ok_prefix = case_prefix + "_ok"

        for file in files:
            if file.startswith(ok_prefix) is True:
                file_path = os.path.join(mapping_sample, file)
                if TestRunner.validator.validate_file(file_path, verbose=False) is False:
                    TestRunner.validator.validate_file(file_path, verbose=True)
                    logger.error(file + " is not valid, it should be")
                    return  False
                logger.info(file + " is valid: fine")
        return True
    
    @staticmethod
    def testKO(mapping_sample, case_prefix):
 
        ko_prefix = case_prefix + "_ko"
        files = os.listdir(mapping_sample)

        for file in files:
            if file.startswith(ko_prefix) is True:
                file_path = os.path.join(mapping_sample, file)
                if TestRunner.validator.validate_file(file_path , verbose=False) is True:
                    logger.error(file + " is valid, it shouldn't be")
                    return False
                logger.info(file + " is not valid: fine")
        return True

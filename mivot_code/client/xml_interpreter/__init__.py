import sys, os
from mivot_code.utils.logger_setup import LoggerSetup

file_path = os.path.dirname(os.path.realpath(__file__)) 

data_dir = os.path.join(file_path, "../../..", "data")
logger = LoggerSetup.get_logger()
LoggerSetup.set_debug_level()

# make sure to know where we are to avoid issue with relative paths
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Config.__read_config__(config_file)
logger.info("translator package intialized")

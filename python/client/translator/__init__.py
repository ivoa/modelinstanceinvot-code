import sys, os
from utils.logger_setup import LoggerSetup
from utils.file_utils import FileUtils

data_dir =  FileUtils.get_datadir()
project_dir = FileUtils.get_projectdir()
schema_dir = FileUtils.get_schemadir()

logger = LoggerSetup.get_logger()
LoggerSetup.set_debug_level()

# make sure to know where we are to avoid issue with relative paths
os.chdir(os.path.dirname(os.path.realpath(__file__)))

logger.info("client.translator package intialized")

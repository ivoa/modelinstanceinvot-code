import sys, os
from mivot_code.utils.logger_setup import LoggerSetup
from mivot_code.utils.file_utils import FileUtils

data_dir =  FileUtils.get_datadir()
project_dir = FileUtils.get_projectdir()
schema_dir = FileUtils.get_schemadir()
schema_path = os.path.join(schema_dir, "merged-syntax.xsd")
schema_url = "https://raw.githubusercontent.com/ivoa-std/ModelInstanceInVot/master/schema/xsd/merged-syntax.xsd"
logger = LoggerSetup.get_logger()
LoggerSetup.set_debug_level()

# make sure to know where we are to avoid issue with relative paths
os.chdir(os.path.dirname(os.path.realpath(__file__)))

logger.info("client package intialized")

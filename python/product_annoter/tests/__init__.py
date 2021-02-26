import sys, os
from utils.file_utils import FileUtils
from utils.logger_setup import LoggerSetup

data_dir =  FileUtils.get_datadir()
project_dir = FileUtils.get_projectdir()
schema_dir = FileUtils.get_schemadir()

logger = LoggerSetup.get_logger()
LoggerSetup.set_debug_level()

# make sure to know where we are to avoid issue with relative paths
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Config.__read_config__(config_file)
logger.info("product_anoter.tests package initialized")

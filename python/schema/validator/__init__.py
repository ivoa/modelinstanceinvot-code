import sys, os
from utils.logger_setup import LoggerSetup
from utils.file_utils import FileUtils

data_dir =  FileUtils.get_datadir()
project_dir = FileUtils.get_projectdir()
schema_dir = FileUtils.get_schemadir()

logger = LoggerSetup.get_logger()
LoggerSetup.set_info_level()

logger.info("utils package intialized")

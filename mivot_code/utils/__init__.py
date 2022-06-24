import sys, os
from mivot_code.utils.logger_setup import LoggerSetup

logger = LoggerSetup.get_logger()
LoggerSetup.set_debug_level()

logger.info("utils package initialized")

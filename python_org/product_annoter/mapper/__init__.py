import sys, os
from utils.logger_setup import LoggerSetup

logger = LoggerSetup.get_logger()
LoggerSetup.set_debug_level()
logger.info("product_anoter.mapper package initialized")

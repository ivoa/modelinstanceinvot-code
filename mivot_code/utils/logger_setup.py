'''
Global logger setup
Must be used by the whole application

The default format can be restored at any time with LoggerSetup.set_default_format()
The log level can be set at any time with LoggerSetup.set_debug/info/warning/error_level
The level is set at INFO by default

Created on 4 December 2019

@author: michel
'''
import sys
import logging


class LoggerSetup:
    """
    manage the logger setup
    """
    __default_level = logging.INFO

    @staticmethod
    def get_logger():
        """
        Format and return the system logger
        :return : system logger
        :rtype: logger
        """
        LoggerSetup.set_default_format()
        return logging.getLogger()

    @staticmethod
    def set_default_format():
        """
        set the default message format
        """
        logging.basicConfig(stream=sys.stdout,
                            format='%(levelname)7s'
                                   ' - [%(filename)s:%(lineno)3s'
                                   ' - %(funcName)10s()] - %(message)s',
                            # datefmt="%Y-%m-%d %H:%M:%S"
                            )
        LoggerSetup.restore_default_level()

    @staticmethod
    def restore_default_level():
        """
        restore the message level with the last value set by a setter
        INFO by default
        """
        logging.getLogger().setLevel(LoggerSetup.__default_level)

    @staticmethod
    def set_debug_level():
        """
        Switch to debug level
        """
        LoggerSetup.__default_level = logging.DEBUG
        logging.getLogger().setLevel(logging.DEBUG)

    @staticmethod
    def set_info_level():
        """
        Switch to info level
        """
        LoggerSetup.__default_level = logging.INFO
        logging.getLogger().setLevel(logging.INFO)

    @staticmethod
    def set_warning_level():
        """
        Switch to warning level
        """
        LoggerSetup.__default_level = logging.WARN
        logging.getLogger().setLevel(logging.WARN)

    @staticmethod
    def set_error_level():
        """
        Switch to error level
        """
        LoggerSetup.__default_level = logging.ERROR
        logging.getLogger().setLevel(logging.ERROR)

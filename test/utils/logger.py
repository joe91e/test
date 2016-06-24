from abc import ABCMeta, abstractmethod
import constants
from io import StringIO
import logging

class LoggerAbstract(object):
    __metaclass__ = ABCMeta

    def __init__(self, logger, config=None, filename=None):
        self._logger = logger
        self._config = config
        self._filename = filename
        self.setup()

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def log(self, message, severity='info'):
        pass

    @abstractmethod
    def get_logger(self):
        pass


class LoggerFile(LoggerAbstract):
    def setup(self):
        """
        this needs to be updated so that we setup the FileHandler
        using the filename provided by the config object.
        """
        self._logger.setLevel(logging.INFO)
        self._handler = logging.FileHandler(self._filename)
        self._logger.addHandler(self._handler)

    def log(self, message, severity='info'):
        if severity == 'info':
            self._logger.info(message)
        elif severity == 'debug':
            self._logger.debug(message)
        elif severity == 'warn':
            self._logger.warn(message)
        elif severity == 'error':
            self._logger.error(message)
        elif severity == 'critical':
            self._logger.critical(message)

    def get_logger(self):
        return self._logger


class LoggerStream(LoggerAbstract):
    """
    This logger option allows all log entries to be logged
    into a string buffer, so that we can print it out at once
    or return to the REST API client for debugging purposes.
    """

    def setup(self):
        self._log_capture_string = StringIO()
        self._handler = logging.StreamHandler(self._log_capture_string)
        self._logger.addHandler(self._handler)

    def log(self, message, severity='info'):
        if severity == 'info':
            self._logger.info(message)
        elif severity == 'debug':
            self._logger.debug(message)
        elif severity == 'warn':
            self._logger.warn(message)
        elif severity == 'error':
            self._logger.error(message)
        elif severity == 'critical':
            self._logger.critical(message)

    def get_logger(self):
        return self._logger

    def get_log_contents(self):
        return self._log_capture_string.getvalue()


class LoggerFactory:
    @staticmethod
    def create(log_type, filename=''):
        if log_type == 'file':
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            print(filename)
            return LoggerFile(logger, None, filename)
        elif log_type == 'stream':
            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            return LoggerStream(logger)
        else:
            raise TypeError('Unknown Factory.')

"""
#usage
if __name__ == '__main__':
    log_stream = LoggerFactory.create('stream')
    log_stream.log("test")
    log_stream.log("test2")
    print log_stream.get_log_contents()
"""

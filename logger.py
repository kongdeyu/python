#coding:utf-8


import logging
from logging import handlers
import os


class Logger(object):

    def __init__(
            self,
            log_name,
            log_dir,
            level,
            backup_count):
        self.log_path = os.path.join(log_dir, log_name)
        self.level = level
        self.__create_log_directory(log_dir)
        self.__init_logger(backup_count)

    # private attribute
    def __create_log_directory(self, log_dir):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def __init_logger(self, backup_count):
        logger = logging.getLogger()
        handler = logging.handlers.TimedRotatingFileHandler(
            self.log_path,
            when='midnight',
            interval=1,
            backupCount=backup_count)
        formatter = logging.Formatter(
            '[%(asctime)s] '
            '[%(levelname)s] '
            '[%(threadName)s] '
            '[%(module)s:%(lineno)d] '
            '%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.level)


class Error(Exception):
    pass

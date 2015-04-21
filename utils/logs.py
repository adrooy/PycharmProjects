#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'limingdong'
__doc__ = """用来记录debug级别以上的日志信息"""

import logging
import os


class Log:
    """
        This class definition a log file
        : Example:
            Log( 'debug.log' )

    """
    def __init__(self, filename):
        BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        self.LOGS_DIR = os.path.join(BASE_DIR, 'logs', filename)
        print self.LOGS_DIR

    def get_logger(self):
        """
            Return logger
        """
        # 创建logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(self.LOGS_DIR)
        file_handler.setLevel(logging.DEBUG)
        # 创建handler,用于输出到控制台
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # 定义handler输出格式
        formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')
        # formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

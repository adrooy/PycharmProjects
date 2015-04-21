#!/usr/bin/env python
#-*- coding: utf-8 -*-


"""
File: log.py
Author: xiangxiaowei
Date: 03/03/15
Description: log
"""


import os
import logging

#reload(sys)
#sys.setdefaultencoding("utf-8")


# 创建logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# 创建handler，用于写入文件
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_DIR = os.path.join(BASE_DIR, 'check_version.log')
print LOGS_DIR
#LOGS_DIR = 'log\\360_minutes_%s.log' % get_date()
file_handler = logging.FileHandler(LOGS_DIR.replace(' ','_'))
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

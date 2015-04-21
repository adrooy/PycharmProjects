#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: main.py
Author: xiangxiaowei
Date: 4/20/2015
Description: GG助手游戏入库
"""

import re
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
from utils.logs import Log
from database import insert, select
import requests

log = Log('a.log')
logger = log.get_logger()


def handle_download_url(upload_data):
    print '222'
    download_url = upload_data['baidupan_url']
    print upload_data['apk_info']
    file_size = upload_data['apk_info']['file_size']
    print file_size
    resp = requests.post(download_url, timeout=10).content
    download_title = re.search(r'<title>(.*)</title>', resp)
    #判断下载链接的文件类型，用于wap站详情页的下载按钮提示
    print '123'
    if 'pan.baidu.com' in download_url:
        download_url_type = 2
        if 'gazip' in download_title.group():
            file_type = 2
        if 'apk' in download_title.group():
            file_type = 1
        #判断下载链接是否和真实文件一直（通过比较文件的大小来区分）
        if file_size in resp:
            flag = 1
        else:
            flag = 0
    else:
        download_url_type = 1
        file_type = 1
    print '234'
    upload_data['apk_info']['file_type'] = file_type
    upload_data['apk_info']['download_url_type'] = download_url_type
    #    return download_url_type, file_type, flag


def upload_game_from_mgmt(upload_id, save_user):
    logger.debug('')
    upload_data = select.get_iplay_upload_game(upload_id)
    print upload_data
    handle_download_url(upload_data)
    print upload_data
    #insert.update_iplay_upload_game_baidupan(upload_data)


def upload_game_from_google(upload_id, save_user):
    pass


def upload_game_from_web(upload_id, save_user):
    pass


def main(argvs):
    """
        确定入库方式: flag==1 所有信息由后台人工填写; flag==2 详情页信息从GooglePlay抓取; flag==3 详情页信息从国内网站(豌豆荚，360等)抓取;
    :param argvs:
    :return:
    """
    """
    :param argvs:
    :return:
    """
    logger.debug('START')
    try:
        flag = argvs[1]
        upload_id = argvs[2]
        save_user = argvs[3]
        if flag == '1':
            upload_game_from_mgmt(upload_id, save_user)
        if flag == '2':
            upload_game_from_google(upload_id, save_user)
        if flag == '3':
            upload_game_from_web(upload_id, save_user)
    except Exception as e:
        logger.debug(e)
    logger.debug('END')
    logger.debug('/n/n/n')


if __name__ == '__main__':
    sys.argv = ['upload_game.py', '1', '3395', '湿主别慌']
    main(sys.argv)
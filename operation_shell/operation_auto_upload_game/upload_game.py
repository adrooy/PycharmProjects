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
import time
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
from utils.logs import Log
from utils.utils import gen_label_info_id, gen_pkg_info_id, format_install_num, format_star_num
from utils.config import GPU_VENDER
from database import insert, select
import requests
from crawler_4_api import get_data_from_googleplayAPI
from crawler_4_api.step03_02_upload_image_to_qiniu import step03_02_01_download_images
from crawler_4_api.step03_02_upload_image_to_qiniu import step03_02_02_upload_images
from crawler_4_api.step03_02_upload_image_to_qiniu import step03_02_03_update_image_url
from crawler_4_web import get_data_from_web


log = Log('upload_game.log')
logger = log.get_logger()


"""
    errors['202']='apk_id生成错误'
    errors['201']='上传的百度盘文件大小和分析出的大小不一致'
    errors['404']='其他错误'
    errors['301']='爬去google信息失败'
    errors['302']='下载的google图片失败'
    errors['303']='上传图片至七牛失败'
    errors['304']='更新图片信息到数据库失败'
    errors['399']='Google游戏上传成功'
    errors['101']='爬去渠道详情也失败，请检查详情页地址是否正确或这是否被封禁'
    errors['102']='分析详情页失败，可能页面改版或者选择的上传渠道和详情页地址不匹配'
    errors['103']='获取label和pkg信息失败'
    errors['104']='插入游戏数据失败'
    errors['105']='游戏下载地址为空'
    errors['106']='渠道内下载地址apk大小和解析的apk大小不一致'
    errors['199']='国内游戏上传成功'
"""


def handle_download_url(upload_data):
    download_url = upload_data['baidupan_url']
    file_size = upload_data['apk_info']['file_size']
    resp = requests.post(download_url, timeout=10).content
    download_title = re.search(r'<title>(.*)</title>', resp)
    #判断下载链接的文件类型，用于wap站详情页的下载按钮提示
    if 'pan.baidu.com' in download_url:
        download_url_type = 2
        if 'gazip' in download_title.group():
            file_type = 2
        if 'apk' in download_title.group():
            file_type = 1
        #判断下载链接是否和真实文件一致（通过比较文件的大小来区分）
        if file_size not in resp:
            raise Exception('文件大小不一致!')
    else:
        #默认直接下载链接的文件都为apk文件
        download_url_type = 1
        file_type = 1
    upload_data['apk_info']['file_type'] = file_type
    upload_data['apk_info']['download_url_type'] = download_url_type


def upload_game_from_mgmt(apk_info):
    """
    :param apk_info:
    :return:
    """
    #初始化apk_info，后台选择入库方式为页面的时候需要在apk_info中插入如下信息
    apk_info['update_desc'] = '1234update_desc'
    apk_info['game_name'] = 'tesr'
    apk_info['icon_url'] = '23232'
    apk_info['screen_shot_urls'] = '333333'
    apk_info['detail_desc'] = '!!1233333333'
    apk_info['game_language'] = '3232'
    apk_info['developer'] = '32323'
    try:
        game_name = apk_info['game_name']
        downloaded_cnts = apk_info.get('downloaded_cnts', 0)
        game_language = apk_info.get('game_language', '')
        screen_shot_urls = apk_info.get('screen_shot_urls', '')
        icon_url = apk_info.get('icon_url', '')
        game_desc = apk_info.get('game_desc', '')
        game_types = apk_info.get('game_types', '')
        developer = apk_info.get('developer', '')
        star_num = apk_info.get('star_num', 0)

        pkg_info = {}
        label_info = {}

        pkg_info['apk_id'] = apk_info['apk_id']
        pkg_info['game_id'] = apk_info['gameid']
        pkg_info['market_channel'] = apk_info['channel']
        pkg_info['game_name'] = game_name
        pkg_info['pkg_name'] = apk_info['pkg_name']
        pkg_info['ver_code'] = apk_info['ver_code']
        pkg_info['ver_name'] = apk_info['ver_name']
        pkg_info['file_size'] = apk_info['file_size']
        pkg_info['download_url'] = apk_info['download_url']
        pkg_info['game_desc'] = game_desc
        pkg_info['downloaded_cnts'] = downloaded_cnts
        pkg_info['game_language'] = game_language
        pkg_info['screen_shot_urls'] = screen_shot_urls
        pkg_info['icon_url'] = icon_url
        pkg_info['min_sdk'] = apk_info['min_sdk']
        pkg_info['download_url_type'] = apk_info['download_url_type']
        pkg_info['source'] = apk_info['source']
        pkg_info['signature_md5'] = apk_info['signature_md5']
        pkg_info['file_md5'] = apk_info['file_md5']
        pkg_info['origin_types'] = game_types
        pkg_info['gpu_vender'] = apk_info['gpu_vender']
        pkg_info['ver_code_by_gg'] = apk_info['ggvercode']
        pkg_info['update_desc'] = apk_info['update_desc']
        pkg_info['file_type'] = apk_info['file_type']
        pkg_info['save_user'] = apk_info['save_user']
        pkg_info['now'] = int(time.time())

        label_info['game_id'] = apk_info['gameid']
        label_info['game_name'] = game_name
        label_info['screen_shot_urls'] = screen_shot_urls
        label_info['icon_url'] = icon_url
        label_info['detail_desc'] = game_desc
        label_info['game_language'] = game_language
        label_info['file_size'] = apk_info['file_size']
        label_info['ver_name'] = apk_info['ver_name']
        label_info['source'] = apk_info['source']
        label_info['origin_types'] = game_types
        label_info['developer'] = developer
        label_info['save_user'] = apk_info['save_user']
        label_info['enabled'] = 0
        label_info['now'] = int(time.time())
        label_info['downloaded_cnts'] = downloaded_cnts
        label_info['star_num'] = star_num
        logger.debug('后台 获取数据 SUCCESS')
    except Exception as e:
        logger.debug('后台 获取数据 ERROR: %s' % e)
        return 501
    try:
        insert.insert_label_info(label_info)
        pkg_info['url4details'] = ''
        insert.insert_pkg_info(pkg_info)
        insert.check_developer(label_info['developer'])
        logger.debug('后台 插入数据 SUCCESS: game_id: %s, apk_id: %s' % (label_info['game_id'], pkg_info['apk_id']))
    except Exception as e:
        logger.debug('后台 插入数据 ERROR: %s' % e)
        return 502
    return 599


def upload_game_from_google(apk_info):
    """
    step_03_01 从googleAPI获取详情页信息
    step_03_02 游戏信息入库iplay_game_label_info和iplay_game_pkg_info
    step_03_03
    :param apk_info:
    :param save_user:
    :return:
    """
    try:
        label_info, pkg_info = get_data_from_googleplayAPI.main(apk_info)
        logger.debug('Google 抓取数据 SUCCESS')
    except Exception as e:
        logger.debug('Google 抓取数据 ERROR: %s' % e)
        return 301
    try:
        label_info['star_num'] = format_star_num(str(label_info['star_num']), 2)
        label_info['downloaded_cnts'] = format_install_num(label_info['downloaded_cnts'])
        insert.insert_label_info(label_info)
        pkg_info['downloaded_cnts'] = format_install_num(pkg_info['downloaded_cnts'])
        pkg_info['url4details'] = "https://play.google.com/store/apps/details?id=%s" % pkg_info['pkg_name']
        insert.insert_pkg_info(pkg_info)
        #厂商入库
        insert.check_developer(label_info['developer'])
        logger.debug('Google 插入数据 SUCCESS: game_id: %s, apk_id: %s' % (label_info['game_id'], pkg_info['apk_id']))
    except Exception as e:
        logger.debug('Google 插入数据 ERROR: %s' % e)
        return 305
    try:
        game_id = apk_info['gameid']
        step03_02_01_download_images.main(game_id)
        logger.debug('Google 下载图片 SUCCESS: game_id: %s, apk_id: %s' % (label_info['game_id'], pkg_info['apk_id']))
        time.sleep(2)
    except Exception as e:
        logger.debug('Google 下载图片 ERROR: %s', str(e.args))
        return 302
    try:
        step03_02_02_upload_images.main()
        logger.debug('Google 上传图片 SUCCESS: game_id: %s, apk_id: %s' % (label_info['game_id'], pkg_info['apk_id']))
        time.sleep(2)
    except Exception as e:
        logger.debug('Google 上传图片 ERROR: %s', str(e.args))
        return 303
    try:
        game_id = apk_info['gameid']
        step03_02_03_update_image_url.execute(game_id)
        logger.debug('Google 更新图片 SUCCESS: game_id: %s, apk_id: %s' % (label_info['game_id'], pkg_info['apk_id']))
        time.sleep(2)
    except Exception as e:
        logger.debug('Google 更新图片 ERROR: %s', str(e.args))
        return 304
    return 399


def upload_game_from_web(apk_info):
    """
    :param apk_info:
    :return:
    """
    try:
        get_data_from_web.main(apk_info)
        label_info, pkg_info = get_data_from_web.main(apk_info)
        logger.debug('WEB 抓取数据 SUCCESS')
    except Exception as e:
        logger.debug('WEB 抓取数据 ERROR: %s' % e)
        return 103
    try:
        insert.insert_label_info(label_info)
        pkg_info['url4details'] = apk_info['detail_url']
        insert.insert_pkg_info(pkg_info)
        insert.check_developer(label_info['developer'])
        logger.debug('WEB 插入数据 SUCCESS: game_id: %s, apk_id: %s' % (label_info['game_id'], pkg_info['apk_id']))
    except Exception as e:
        logger.debug('WEB 插入数据: %s' % e)
        return 104
    return 199


def upload(argvs):
    """
        确定入库方式: flag==4 详情页信息从国内网站(豌豆荚，360等)抓取; flag==3 详情页信息从GooglePlay抓取; flag==1 详情页信息从后台页面获取;
    :param argvs: ['upload_game.py', flag(入库方式), upload_id(入库记录信息id), save_user(入库人)]; example: [ 'upload_game.py', '1', '3395', '湿主别慌']
    :return: msg (199, 201, ...)
    """
    #try:
    if 1==1:
        flag = argvs[1]
        upload_id = argvs[2]
        save_user = argvs[3]
        channels = select.get_channel_mapping()
        upload_data = select.get_iplay_upload_game(upload_id)
        upload_data['apk_info'] = eval(upload_data['apk_info'])
        upload_data['apk_info']['channel'] = channels[upload_data['apk_info']['channelid']]
        upload_data['apk_info']['gpu_vender'] = GPU_VENDER[upload_data['apk_info']['channelid']] if upload_data['apk_info']['channelid'] in GPU_VENDER else 1
        upload_data['apk_info']['source'] = upload_data['source']
        upload_data['apk_info']['save_user'] = save_user
        upload_data['apk_info']['download_url'] = upload_data['baidupan_url']
        upload_data['apk_info']['detail_url'] = upload_data['detail_url']
        pkg_name = upload_data['apk_info']['pkg_name']
        ver_name = upload_data['apk_info']['ver_name']
        channel = upload_data['apk_info']['channel']
        ver_code_by_gg = upload_data['apk_info']['ggvercode']
        try:
            handle_download_url(upload_data)
            logger.debug('STEP_01 SUCCESS handle_download_url')
        except Exception as e:
            logger.debug('handle_download_url: %s' % e)
            upload_data['msg'] = 201
            return upload_data
        try:
            apk_id = gen_pkg_info_id(pkg_name, ver_name, channel, ver_code_by_gg)
            upload_data['apk_id'] = apk_id
            upload_data['apk_info']['apk_id'] = apk_id
            upload_data['game_id'] = upload_data['apk_info']['gameid']
            logger.debug('STEP_02 SUCCESS gen_pkg_info_id')
        except Exception as e:
            logger.debug('gen_pkg_info_id: %s' % e)
            upload_data['msg'] = 202
            return upload_data
        apk_info = upload_data['apk_info']
        if flag == '1':
            msg = upload_game_from_mgmt(apk_info)
        if flag == '3':
            msg = upload_game_from_google(apk_info)
        if flag == '4':
            msg = upload_game_from_web(apk_info)
        upload_data['msg'] = msg
        return upload_data
    #except Exception as e:
        logger.debug('upload: %s' % e)
        upload_data['msg'] = 404
        return upload_data


def main(argvs):
    logger.debug('START')
    upload_data = upload(argvs)
    upload_data['now'] = int(time.time())
    upload_data['is_finished'] = 1
    upload_data['channel'] = upload_data['apk_info']['channel']
    insert.update_iplay_upload_game(upload_data)
    logger.debug('END')
    logger.debug('\n\n\n')


if __name__ == '__main__':
    sys.argv = ['upload_game.py', '3', '3331', '湿主别慌']
    main(sys.argv)
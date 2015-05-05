#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: analyze_main.py
Author: limingdong
Date: 7/28/14
Description: 
"""

import os
import sys
import time
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
import requests
import wandoujia


def perpare_data(info, apk_info):
    if not info:
        return
    game_name = info['game_name']
    downloaded_cnts = info.get('downloaded_cnts', 0)
    game_language = info.get('game_language', '')
    screen_shot_urls = info.get('screen_shot_urls', '')
    icon_url = info.get('icon_url', '')
    game_desc = info.get('game_desc', '')
    game_types = info.get('game_types', '')
    developer = info.get('developer', '')
    star_num = info.get('star_num', 0)

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
    return label_info, pkg_info


def execute(web, html):
    choose = {
    #    "360": qihoo360.analyze,
    #    "91": apk91.analyze,
     #   "安卓市场": hiapk.analyze,
    #    "小米": xiaomi.analyze,
     #   "应用宝": yingyongbao.analyze,
     #   "百度": baidu.analyze,
        "豌豆荚": wandoujia.analyze,
    }
    info = choose.get(web)(str(html))
    return info


def get_html_from_detail_url(detail_url):
    html = requests.post(detail_url, timeout=10).content
    html = html.replace("false", "False")
    html = html.replace("null", "None")
    return html


def main(apk_info):
    detail_url = apk_info['detail_url']
    html = get_html_from_detail_url(detail_url)
    if 'www.wandoujia.com' in detail_url:
        web = '豌豆荚'
    info = execute(web, html)
    label_info, pkg_info = perpare_data(info, apk_info)
    return label_info, pkg_info


#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import json
import time
from config import *
from googleplay import GooglePlayAPI
from jianfan import ftoj


reload(sys)
sys.setdefaultencoding('utf-8')
cur_dir = os.path.abspath(os.path.dirname(__file__))


google_game_type = {
    'GAME_STRATEGY': '经营策略',
    'GAME_ACTION': '动作射击',
    'GAME_CASINO': '扑克棋牌',
    'GAME_FAMILY': '休闲时间',
    'GAME_ROLE_PLAYING': '角色扮演',
#    'GAME_EDUCATIONAL': '儿童益智',
    'GAME_EDUCATIONAL': '休闲时间',
    'GAME_ARCADE': '体育格斗',
    'GAME_PUZZLE': '休闲时间',
    'GAME_RACING': '跑酷竞速',
    'GAME_CARD': '扑克棋牌',
    'GAME_ADVENTURE': '角色扮演',
    'GAME_SIMULATION': '休闲时间',
    'GAME_SPORTS': '体育格斗',
    'GAME_WORD': '休闲时间',
    'GAME_CASUAL': '休闲时间',
    'GAME_TRIVIA': '休闲时间',
    'GAME_MUSIC': '休闲时间',
    'GAME_BOARD': '扑克棋牌',
    'ENTERTAINMENT': '休闲时间'
}


def login():
    api = None
    try:
        api = GooglePlayAPI(ANDROID_ID)
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
    except Exception as e:
        print e
    return api


def get_info(api, pkg_name):
    details = None
    try:
        details = api.details(pkg_name)
    except Exception as e:
        print "Error: something went wrong?"
        print e
    return details


def write_file(pkg_name, info):
    #cur_dir = os.getcwd()
    dir_google = os.path.join(cur_dir, 'data')
    data_path = os.path.join(dir_google, '%s.json' % pkg_name)
    if not os.path.exists(dir_google):
        os.makedirs(dir_google)
    with open(data_path, 'w') as data:
        data.write(json.dumps(info, ensure_ascii=False))


def get_game_info(pkg_name):
    dir_google = os.path.join(cur_dir, 'data')
    data_path = os.path.join(dir_google, '%s.json' % pkg_name)
    doc = dict()
 
    if os.path.isfile(data_path):
        with open(data_path, 'r') as data:
            info = data.read().strip()
            if info:
                info = info.replace("true", "True")
                info = info.replace("false", "False")
                doc = eval(info)
    if not doc:
        api = login()
        info = get_info(api, pkg_name)
        info = api.toDict(info)
        info = str(info)
        info = info.replace("true", "True")
        info = info.replace("false", "False")
        doc = eval(str(info))
        write_file(pkg_name, doc)
    return doc


def perpare_data(info, apk_info):
    if not info:
        return
    doc = info["docV2"]
    game_name = doc["title"]
    game_desc = doc["descriptionHtml"]
    if game_desc:
        game_desc = game_desc.replace("<br>", "\n").replace("<p>", "\n").replace("<p>", "\n")
    app_details = doc['details']['appDetails']
    game_types = app_details["appCategory"][0]
    try:
        game_types = google_game_type[game_types]
    except:
        game_types = '其他'
    downloaded_cnts = doc["details"]["appDetails"]["numDownloads"]
    developer = doc['details']['appDetails']['developerName']
    game_language = "多国语言"
    screen_shot_urls = ""
    icon_url = ""
    images = doc["image"]
    if images:
        for image in images:
            image_type = image["imageType"]
            image_url = image["imageUrl"]
            if image_type == 4:
                icon_url = image_url
            if image_type == 1:
                screen_shot_urls += image_url + "\n"
    star_num = doc["aggregateRating"]["starRating"]
    #将繁体中文改为简体
    game_name = ftoj(game_name)
    game_desc = ftoj(game_desc)
    developer = ftoj(developer)

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


def main(apk_info):
    pkg_name = apk_info['pkg_name']
    doc = get_game_info(pkg_name)
    label_info, pkg_info = perpare_data(doc, apk_info)
    return label_info, pkg_info
 

if __name__ == "__main__":
    pkg_name = 'com.disney.disneyinfinity2_goo'
    print cur_dir
    doc = get_game_info(pkg_name, detail_url)
    print doc

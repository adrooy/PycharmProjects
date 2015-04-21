#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: search_by_pkg_name.py
Author: limingdong
Date: 8/14/14
Description: 根据包名获取游戏信息
"""


import sys
import time
import utils
import db
import os
import json
from config import *
from googleplay import GooglePlayAPI
from jianfan import ftoj
from logs import logger


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


def perpare_data(info, download_url, file_size, ver_code, ver_name, channel, apk_info):
    if not info:
        return
    doc = info["docV2"]
    #if channel == "GG官方":
    market_channel = channel
    if channel == "samsung":
         market_channel = "三星"
    game_name = doc["title"]
    pkg_name = apk_info["pkg_name"]
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
    utils.check_developer(developer)
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

    is_crack_apk = 1  # 破解版
    min_sdk = ""
    star_num = doc["aggregateRating"]["starRating"]
    now = str(int(time.time()))

    label_info = dict()
    pkg_info = dict()

    game_name = ftoj(game_name)
    game_desc = ftoj(game_desc)
    
    #if channel == "GG官方":
    g_name = game_name + u"(%s)" % channel
    if channel == "samsung":
          g_name = game_name + u"(samsung)"
    #g_name = game_name + u"(GG官方)"
    #adrooy
    #g_name = game_name + u"(samsung)"
    game_id = utils.gen_label_info_id(g_name)
    g_name = g_name.replace(u"(GG官方)", "")
    if ver_name:
        ver_name = filter(lambda ch: ch in '0123456789.', ver_name)
    if 'gameid' in apk_info:
        game_id = apk_info['gameid']
    label_info["game_id"] = game_id
    label_info["game_name"] = g_name
    label_info["game_types"] = game_types
    label_info["origin_types"] = game_types
    label_info["screen_shot_urls"] = screen_shot_urls
    label_info["icon_url"] = icon_url
    label_info["detail_desc"] = game_desc
    label_info["star_num"] = utils.format_star_num(str(star_num), 2)
    label_info["download_counts"] = utils.format_install_num(downloaded_cnts)
    label_info["game_language"] = game_language
    label_info["now"] = now
    label_info["file_size"] = file_size
    label_info["ver_name"] = ver_name
    label_info["developer"] = developer

    pkg_info["market_channel"] = market_channel
    pkg_info["game_name"] = g_name
    pkg_info["pkg_name"] = pkg_name
    pkg_info["ver_code"] = ver_code
    pkg_info["ver_name"] = ver_name
    pkg_info["file_size"] = file_size
    pkg_info["download_urls"] = download_url.strip()
    pkg_info["game_desc"] = game_desc
    pkg_info["game_types"] = game_types
    pkg_info["origin_types"] = game_types
    pkg_info["downloaded_cnts"] = utils.format_install_num(downloaded_cnts)
    pkg_info["game_language"] = game_language
    pkg_info["screen_shot_urls"] = screen_shot_urls
    pkg_info["icon_url"] = icon_url
    pkg_info["now"] = now
    pkg_info["is_crack_apk"] = is_crack_apk
    if "ggvercode" not in apk_info:
        apk_info["ggvercode"] = "null"
    apk_id = utils.gen_pkg_info_id(0, pkg_name, ver_name, market_channel, apk_info["ggvercode"])
    pkg_info["apk_id"] = apk_id
    pkg_info["game_id"] = game_id
    pkg_info["url4details"] = "https://play.google.com/store/apps/details?id=%s" % pkg_name
    #print apk_id, game_id
    #import sys
    #sys.exit()
    return label_info, pkg_info


def write_file(pkg_name, info):
    #cur_dir = os.getcwd()
    dir_google = os.path.join(cur_dir, 'data')
    data_path = os.path.join(dir_google, '%s.json' % pkg_name)
    if not os.path.exists(dir_google):
        os.makedirs(dir_google)
    with open(data_path, 'w') as data:
        data.write(json.dumps(info, ensure_ascii=False))


def get_game_info(pkg_name, detail_url):
    #cur_dir = os.getcwd()
    dir_google = os.path.join(cur_dir, 'data')
    data_path = os.path.join(dir_google, '%s.json' % pkg_name)
    doc = dict()
    #print 'adr'
    #print detail_url
    #print data_path
 
    if os.path.isfile(data_path):
        with open(data_path, 'r') as data:
            info = data.read().strip()
            if info:
                info = info.replace("true", "True")
                info = info.replace("false", "False")
                doc = eval(info)
    if not doc:
        api = login()
        #xiangxiaowei
        #if pkg_name == 'com.gameloft.android.GAND.GloftA8SS':
        #    pkg_name = 'com.gameloft.android.ANMP.GloftA8HM'
        if detail_url:
            info = get_info(api, detail_url)
        else: 
            info = get_info(api, pkg_name)
        info = api.toDict(info)
        info = str(info)
        info = info.replace("true", "True")
        info = info.replace("false", "False")
        doc = eval(str(info))
    #print doc
    #import sys
    #sys.exit()
    return doc


def execute(pkg_name, cert_md5, file_md5, min_sdk, download_url, short_desc, file_size, ver_code, ver_name, detail_url, channel, apk_info):

    doc = get_game_info(pkg_name, detail_url)
    label_info, pkg_info = perpare_data(doc, download_url, file_size, ver_code, ver_name, channel, apk_info)
    pkg_info["signature_md5"] = cert_md5
    pkg_info["file_md5"] = file_md5
    pkg_info["min_sdk_version"] = min_sdk
    pkg_info["game_desc"] = pkg_info["game_desc"]
    #xiangxiaowei
    pkg_info["pkg_name"] = pkg_name
    pkg_info["gpu_vender"] = apk_info["gpu_vender"]
    pkg_info["update_desc"] = apk_info["update_desc"]
    pkg_info["ver_code_by_gg"] = apk_info["ggvercode"]
    pkg_info["save_user"] = apk_info["save_user"]
    pkg_info["ver_name"] = apk_info["ver_name"]

    label_info["short_desc"] = short_desc
    label_info["detail_desc"] = label_info["detail_desc"]
    label_info["save_user"] = apk_info["save_user"]

    if label_info and pkg_info:
        pkg_name = pkg_info["pkg_name"]

        # 记录游戏信息
        write_file(pkg_name, doc)

        # 插入google play游戏信息
        db.insert_label_info(label_info)
        db.insert_pkg_info(pkg_info)
        logger.info("insert game_id: %s, name: %s", label_info["game_id"], label_info["game_name"])


def main(apk_info, channel, detail_url):
    pkg_name = apk_info['pkg_name']
    cert_md5 = apk_info['signature_md5']
    file_md5 = apk_info['file_md5']
    min_sdk = apk_info['min_sdk']
    download_url = apk_info['baidupan_url']
    file_size = apk_info['file_size']
    ver_code = apk_info['ver_code']
    ver_name = apk_info['ver_name']
    execute(pkg_name, cert_md5, file_md5, min_sdk, download_url, '', file_size, ver_code, ver_name, detail_url, channel, apk_info)


if __name__ == "__main__":
    main('')

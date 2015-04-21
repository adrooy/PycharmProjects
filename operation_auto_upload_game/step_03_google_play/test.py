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
from database.mysql_client import connections


reload(sys)
sys.setdefaultencoding('utf-8')

google_game_type = {
    'GAME_STRATEGY': '经营策略',
    'GAME_ACTION': '动作射击',
    'GAME_CASINO': '扑克棋牌',
    'GAME_FAMILY': '休闲时间',
    'GAME_ROLE_PLAYING': '角色扮演',
    'GAME_EDUCATIONAL': '儿童益智',
    'GAME_ARCADE': '体育格斗',
    'GAME_PUZZLE': '休闲时间',
    'GAME_RACING': '跑酷竞速',
    'GAME_CARD': '扑克棋牌',
    'GAME_ADVENTURE': '经营策略',
    'GAME_SIMULATION': '网络游戏',
    'GAME_SPORTS': '体育格斗',
    'GAME_WORD': '休闲时间',
    'GAME_CASUAL': '休闲时间',
    'GAME_TRIVIA': '儿童益智',
    'GAME_MUSIC': '休闲时间',
    'GAME_BOARD': '扑克棋牌'
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
        sys.exit(1)
    return details


def select_label_info():
    conn = connections('DictCursor')
    cursor = conn.cursor()
    rows = tuple()
    try:
        sql = """
        SELECT label.game_id, pkg.pkg_name  FROM forum.iplay_game_label_info label
        LEFT JOIN forum.iplay_game_pkg_info pkg ON pkg.game_id = label.game_id
        WHERE label.`source` = 3
        """
        cursor.execute(sql)
        rows = cursor.fetchall()
        print len(rows)
    except Exception as e:
        logger.debug("select_label_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def udpate_label_info(info):
    conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        label_sql = """
            UPDATE iplay_game_label_info
            SET developer = %(developer)s
            where game_id = %(game_id)s;
        """
        cursor.execute(label_sql, info)
        conn.commit()
        print "update game_id: %s success." % info['game_id']
    except Exception as e:
        conn.rollback()
        logger.debug("udpate_label_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def perpare_data(info):
    if not info:
        return
    doc = info["docV2"]
    developer = doc['details']['appDetails']['developerName']
    versionCode = doc['details']['appDetails']['versionCode']
    print versionCode
    print developer
    print doc.keys()
    print doc['aggregateRating']
    return developer


def write_file(pkg_name, info):
    cur_dir = os.getcwd()
    dir_google = os.path.join(cur_dir, 'data')
    data_path = os.path.join(dir_google, '%s.json' % pkg_name)
    if not os.path.exists(dir_google):
        os.makedirs(dir_google)
    with open(data_path, 'w') as data:
        data.write(json.dumps(info, ensure_ascii=False))


def get_game_info(pkg_name):
    cur_dir = os.getcwd()
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
        time.sleep(30)
    return doc


def execute(game_id, pkg_name):

    doc = get_game_info(pkg_name)
    developer = perpare_data(doc)

    info = dict()
    info['game_id'] = game_id
    info['developer'] = developer
    # udpate_label_info(info)
    # 记录游戏信息
    write_file(pkg_name, doc)


def main():
    pkg_name = 'com.disney.wheresmywater2_goo'
    game_id = '19defbd9'
    execute(game_id, pkg_name)
    # labels = select_label_info()
    # for label in labels:
    #     game_id = label.get('game_id')
    #     pkg_name = label.get('pkg_name')
    #     print pkg_name
    #     execute(game_id, pkg_name)


if __name__ == "__main__":
    main()
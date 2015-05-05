#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: select.py
Author: limingdong
Date: 7/10/14
Description: 查询爬取的页面信息
"""

from mysql_client import connections
import os
import sys
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
from utils.logs import Log
log = Log('select.log')
logger = log.get_logger()


def get_crawler_info(channel, name):
    conn = connections('Cursor')
    cursor = conn.cursor()
    sql = "SELECT details FROM crawler_info where channel = %s and name = %s;"
    rows = None
    try:
        cursor.execute(sql, (channel, name,))
        rows = cursor.fetchone()
    except Exception as e:
        logger.debug("get_crawler_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_crawlers_info():
    conn = connections('Cursor')
    cursor = conn.cursor()
    sql = "SELECT id, channel, name, details FROM crawler_info where id > 0 order by id;"
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_crawlers_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_page_list(channel):
    conn = connections('Cursor')
    cursor = conn.cursor()
    sql = "SELECT id, lists FROM games_test.lists_page where channel = %s"
    rows = None
    try:
        cursor.execute(sql, (channel,))
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_crawler_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_iplay_upload_game(upload_id):
    """
    得到入库的基本信息apk_info...
    :param upload_id:
    :return:
    """
    conn = connections('DictCursor')
    cursor = conn.cursor()
    sql = "SELECT * FROM forum.iplay_upload_game where id = %s"
    rows = None
    try:
        cursor.execute(sql, (upload_id,))
        rows = cursor.fetchone()
    except Exception as e:
        logger.debug("get_crawler_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_channel_mapping():
    """
    :return: channels   {'1': 'GG官方', '2': '高通版'...}
    """
    conn = connections('52DictCursor')
    cursor = conn.cursor()
    sql = "SELECT * FROM iplay_tool_channel_mapping"
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_channel_mapping: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    channels = {}
    for row in rows:
        channel_id = str(int(row['id']))
        channel_name = row['name']
        channels[channel_id] = channel_name
    return channels


def get_google_pkg_info(game_id):
    """
    获取需要下载图片的googleplay游戏
    :param game_id:
    :return:
    """
    conn = connections('DictCursor')
    cursor = conn.cursor()
    rows = tuple()
    try:
        sql = """
        SELECT game_id, icon_url, screen_shot_urls
        FROM iplay_game_pkg_info
        # WHERE market_channel = "google"
        WHERE enabled = 1
        AND (icon_url like '%ggpht.com%' or icon_url like '%googleusercontent.com%')
        AND game_id ='""" + game_id + """'"""
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("select_google_pkg_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_google_plugin_info(plugin_id):
    """
    获取需要入库的googleplay插件
    :param plugin_id:
    :return:
    """
    conn = connections('DictCursor')
    cursor = conn.cursor()
    rows = tuple()
    try:
        sql = """
        SELECT target_pkg_name, target_ver_code, editor, id
        FROM iplay_upload_plugin
        WHERE id = %d
        """ % plugin_id
        cursor.execute(sql)
        rows = cursor.fetchone()
    except Exception as e:
        logger.debug("get_google_plugin_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


if __name__ == '__main__':
    row = get_google_plugin_info(4)
    print row

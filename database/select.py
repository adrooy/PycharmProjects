#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: select.py
Author: limingdong
Date: 7/10/14
Description: 查询爬取的页面信息
"""

from mysql_client import connections
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


def test():
    iplay_upload = get_iplay_upload_game(1)
    print iplay_upload
    print type(iplay_upload['apk_info'])

if __name__ == '__main__':
    test()

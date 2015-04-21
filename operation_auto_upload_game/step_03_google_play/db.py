#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: db.py
Author: limingdong
Date: 7/18/14
Description: 
"""

from database.mysql_client import connections
from logs import logger


def insert_label_info(infos):
    """
    数据来源(source),1 抓取数据 2 论坛数据 3 google play 数据
    :param infos:
    """
    conn = connections('RemoteCursor')
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO iplay_game_label_info(
        game_id
        , game_name
        , game_types
        , screen_shot_urls
        , icon_url
        , detail_desc
        , star_num
        , download_counts
        , game_language
        , save_timestamp
        , min_apk_size
        , max_apk_size
        , min_ver_name
        , max_ver_name
        , source
        , short_desc
        , display_name
        , update_timestamp
        , origin_types
        , developer
        , save_user
        , update_user
        ) VALUES (
        %(game_id)s
        , %(game_name)s
        , %(game_types)s
        , %(screen_shot_urls)s
        , %(icon_url)s
        , %(detail_desc)s
        , %(star_num)s
        , %(download_counts)s
        , %(game_language)s
        , %(now)s
        , %(file_size)s
        , %(file_size)s
        , %(ver_name)s
        , %(ver_name)s
        , 3
        , %(short_desc)s
        , %(game_name)s
        , %(now)s
        , %(origin_types)s
        , %(developer)s
        , %(save_user)s
        , %(save_user)s
        ) ON DUPLICATE KEY UPDATE
        enabled = 1
        , icon_url = VALUES(icon_url)
        , save_timestamp = VALUES(save_timestamp)
        , update_timestamp = VALUES(update_timestamp)
        """
        cursor.execute(sql, infos)
        conn.commit()

    except Exception as e:
        conn.rollback()
        logger.debug("insert_label_info name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# def insert_pkg_info(db, infos):
def insert_pkg_info(infos):
    """
    download_url_type: 1普通, 2百度盘
    数据来源(source): 1 抓取数据 2 论坛数据 3 google play 数据, GG官方
    is_plugin_required: 0不需要, 1需要
    :param infos:
    """
    conn = connections('RemoteCursor')
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO iplay_game_pkg_info(
        apk_id
        , game_id
        , market_channel
        , game_name
        , pkg_name
        , ver_code
        , ver_name
        , file_size
        , download_url
        , game_desc
        , game_types
        , downloaded_cnts
        , game_language
        , screen_shot_urls
        , icon_url
        , save_timestamp
        , is_crack_apk
        , min_sdk
        , download_url_type
        , source
        , is_plugin_required
        , signature_md5
        , file_md5
        , update_timestamp
        , origin_types
        , url4details
        , gpu_vender
        , ver_code_by_gg
        , update_desc
        , is_max_version
        , save_user
        ) VALUES (
        %(apk_id)s
        , %(game_id)s
        , %(market_channel)s
        , %(game_name)s
        , %(pkg_name)s
        , %(ver_code)s
        , %(ver_name)s
        , %(file_size)s
        , %(download_urls)s
        , %(game_desc)s
        , %(game_types)s
        , %(downloaded_cnts)s
        , %(game_language)s
        , %(screen_shot_urls)s
        , %(icon_url)s
        , %(now)s
        , %(is_crack_apk)s
        , %(min_sdk_version)s
        , 2
        , 3
        , 1
        , %(signature_md5)s
        , %(file_md5)s
        , %(now)s
        , %(origin_types)s
        , %(url4details)s
        , %(gpu_vender)s
        , %(ver_code_by_gg)s
        , %(update_desc)s
        , 1
        , %(save_user)s
        ) ON DUPLICATE KEY UPDATE
        enabled = 1
        , icon_url = VALUES(icon_url)
        , save_timestamp = VALUES(save_timestamp)
        , update_timestamp = VALUES(update_timestamp)
        , ver_code = VALUES (ver_code)
        , ver_name = VALUES (ver_name)
        , file_size = VALUES (file_size)
        , download_url = VALUES (download_url)
        , gpu_vender = VALUES (gpu_vender)
        """
        cursor.execute(sql, infos)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("insert_pkg_info name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def select_label_info_by_name(game_name):
    conn = connections('RemoteCursor')
    cursor = conn.cursor()
    rows = tuple()
    try:
        sql = """
        SELECT game_id
        FROM iplay_game_label_info
        WHERE game_name like %s
        AND enabled = 1
        """
        cursor.execute(sql, ("%" + game_name + "%",))
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("select_label_info_by_name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def udpate_label_and_pkg_info(game_id):
    conn = connections('RemoteCursor')
    cursor = conn.cursor()
    try:
        label_sql = """
            UPDATE iplay_game_label_info
            SET enabled = 0
            where game_id = %s;
        """
        pkg_sql = """
            UPDATE iplay_game_pkg_info
            SET enabled = 0
            where game_id = %s;
        """
        cursor.executemany(label_sql, game_id)
        cursor.executemany(pkg_sql, game_id)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("udpate_label_and_pkg_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def select_google_pkg_info():
    conn = connections('DictRemoteCursor')
    cursor = conn.cursor()
    rows = tuple()
    try:
#        sql = """
#        SELECT game_id, icon_url, screen_shot_urls
#        FROM iplay_game_pkg_info
#        # WHERE market_channel = "google"
#        WHERE market_channel in ("GG官方", "三星", "高通版", "英伟达", "PowerVR", "Mali", "全球版", "GG官方原包", "三星原包", "高通版原包", "英伟达原包", "PowerVR原包", "Mali原包")
#        AND enabled = 1
#        AND icon_url like '%ggpht.com%'
#        """
        sql = """
        SELECT game_id, icon_url, screen_shot_urls
        FROM iplay_game_pkg_info
        # WHERE market_channel = "google"
        WHERE enabled = 1
        AND icon_url like '%ggpht.com%'
        """
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


def select_google_ver_code():
    conn = connections('DictRemoteCursor')
    cursor = conn.cursor()
    rows = tuple()
    try:
        sql = """
        SELECT pkg_name, max(ver_code) as ver_code FROM forum.iplay_game_pkg_info
        WHERE source = 3
        GROUP BY pkg_name;
        """
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

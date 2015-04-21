#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: insert.py
Author: limingdong
Date: 7/10/14
Description: 
"""


from mysql_client import connections
from utils.logs import Log
log = Log('insert.log')
logger = log.get_logger()


#推广游戏source=4的数据入库
def insert_label_info(infos):
    """
    数据来源(source),1 抓取数据 2 论坛数据 3 google play 数据 4 推广游戏入库
    :param infos:
    """
    conn = connections('Cursor')
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
        , tid
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
        , %(source)s
        , %(short_desc)s
        , %(game_name)s
        , %(now)s
        , %(origin_types)s
        , %(developer)s
        , 0
        , %(save_user)s
        , %(save_user)s
        ) ON DUPLICATE KEY UPDATE
        enabled = 1
        , icon_url = VALUES(icon_url)
        , update_timestamp = VALUES(update_timestamp)
        , save_timestamp = VALUES(save_timestamp)
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


def insert_pkg_info(infos):
    """
    download_url_type: 1普通, 2百度盘
    数据来源(source): 1 抓取数据 2 论坛数据 3 google play 数据, GG官方 4 推广游戏入库
    is_plugin_required: 0不需要, 1需要
    :param infos:
    """
    conn = connections('Cursor')
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
        , tid
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
        , %(source)s
        , 0
        , %(signature_md5)s
        , %(file_md5)s
        , %(now)s
        , %(origin_types)s
        , %(url4details)s
        , %(gpu_vender)s
        , 0
        , %(ver_code_by_gg)s
        , %(update_desc)s
        , 1
        , %(save_user)s
        ) ON DUPLICATE KEY UPDATE
        enabled = 1
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


def insert_iplay_upload_game(infos):
    """
    :param infos:
    """
    conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        sql = """
        INSERT IGNORE INTO iplay_upload_game(
        apk_id,
        start_date,
        source,
        msg
        ) VALUES (
        %(apk_id)s,
        %(now)s,
        %(source)s,
        %(msg)s
        )
        """
        cursor.execute(sql, infos)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("iplay_upload_game name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_iplay_upload_game(infos):
    """
    :param infos:
    """
    conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        sql = """
        UPDATE iplay_upload_game SET
        end_date = %(now)s,
        source = %(source)s,
        is_finished = %(is_finished)s,
        msg = %(msg)s,
        apk_id = %(apk_id)s,
        channel = %(channel)s
        WHERE id = %(id)s
        """
        cursor.execute(sql, infos)
        print sql
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("update_iplay_upload_game name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_iplay_upload_game_baidupan(infos):
    """
    :param infos:百度盘中文件大小不一致,数据库更新
    """
    conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        sql = """
        UPDATE iplay_upload_game SET
        end_date = %(now)s,
        msg = %(msg)s,
        is_finished = %(is_finished)s
        WHERE id = %(id)s
        """
        cursor.execute(sql, infos)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("update_iplay_upload_game_baidupan name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def update_pkg_by_game_id(game_id):
    """
    如果国内游戏选择下载渠道为百度盘,则删除其他渠道游戏信息
    :param infos:
    """
    conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        sql = """
        UPDATE iplay_game_pkg_info SET
        enabled = 0
        WHERE game_id = %s
        """
        cursor.execute(sql, (game_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("update_pkg_by_game_id ERROR: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

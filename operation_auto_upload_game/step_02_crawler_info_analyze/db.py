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


def insert_label_info(conn, infos):
    # conn = connections('Cursor')
    cursor = conn.cursor()
    # game_id = 0
    try:
        sql = """
        INSERT IGNORE INTO iplay_game_label_info(
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
        , display_name
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
        , %(display_name)s
        )
        """
        cursor.execute(sql, infos)
        conn.commit()

    except Exception as e:
        conn.rollback()
        logger.debug("insert_label_info name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        # if conn:
        #     conn.close()


def insert_pkg_info(conn, infos):
    # conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        sql = """
        INSERT IGNORE INTO iplay_game_pkg_info(
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
        )
        """
        cursor.executemany(sql, infos)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("insert_pkg_info name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        # if conn:
        #     conn.close()


def get_crawlers_info(game_name):
    conn = connections('DictCursor')
    cursor = conn.cursor()
    sql = """SELECT id, channel, name, gameName, pkgName, verCode, verName, filesize, downloadUrl, gameDesc, gameTypes,
        screenShotUrls, iconUrl, starNum, downloadCounts, gameLanguage, is_merge
        FROM crawler_info
        WHERE is_parse = 1
        AND is_merge = 0
        AND name = %s
        ORDER BY FIELD(channel, '应用宝', '360', '豌豆荚', '安卓市场', '小米', '91', '百度')
        """
    rows = None
    try:
        cursor.execute(sql, (game_name,))
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_crawlers_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_label_info_id(conn, game_name):
    # conn = connections('Cursor')
    cursor = conn.cursor()
    sql = "SELECT game_id FROM iplay_game_label_info where game_name = %s;"
    game_id = None
    try:
        cursor.execute(sql, (game_name,))
        rows = cursor.fetchone()
        if rows:
            game_id = rows[0]
    except Exception as e:
        logger.debug("get_label_info_id: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        # if conn:
        #     conn.close()
    return game_id


def get_game_name():
    conn = connections('Cursor')
    cursor = conn.cursor()
    sql = "SELECT distinct name FROM crawler_info;"
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_game_name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def update_crawler_info(conn, infos):
    # conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        sql = """
        UPDATE crawler_info SET is_merge = %(is_merge)s
        WHERE id = %(id)s
        """
        # logger.info(infos)
        cursor.executemany(sql, infos)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("update_crawler_info: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        # if conn:
        #     conn.close()


def get_common_pkg_name():
    conn = connections('Cursor')
    cursor = conn.cursor()
    sql = """SELECT pkgName, count(pkgName) as cnt, is_parse, is_merge
        FROM crawler_info
        GROUP BY pkgName
        HAVING cnt>1
        AND is_parse=1
        # AND is_merge=0
        AND pkgName != ""
        AND pkgName IS NOT NULL
        """
    result = []
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            pkg_name = row[0]
            result.append(pkg_name)
    except Exception as e:
        logger.debug("get_common_pkg_name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return result


def get_crawlers_info_by_pkg_name(conn, pkg_name):
    # conn = connections('DictCursor')
    cursor = conn.cursor()
    sql = """SELECT
          id
          , channel
          , name
          , gameName
          , pkgName
          , verCode
          , verName
          , filesize
          , downloadUrl
          , gameDesc
          , gameTypes
          , screenShotUrls
          , iconUrl
          , starNum
          , downloadCounts
          , gameLanguage
          , is_merge
          , min_sdk_version
          , game_tags
          , id_in_channel
          , url4details
          FROM crawler_info
          WHERE is_parse = 1
          # AND is_merge = 0
          AND pkgName = %s
          ORDER BY FIELD(channel, '应用宝', '360', '豌豆荚', '安卓市场', '小米', '91', '百度')
        """
    rows = None
    try:
        cursor.execute(sql, (pkg_name,))
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_crawlers_info_by_pkg_name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        # if conn:
        #     conn.close()
    return rows


SQL_DIFF_PKG_NAME = """
    select
    id
    , channel
    , name
    , gameName
    , pkgName
    , verCode
    , verName
    , filesize
    , downloadUrl
    , gameDesc
    , gameTypes
    , screenShotUrls
    , iconUrl
    , starNum
    , downloadCounts
    , gameLanguage
    , is_merge
    , min_sdk_version
    , game_tags
    , id_in_channel
    , url4details
    FROM crawler_info
    where gameName != ""
    and is_parse = 1
    and is_merge = 0
    order by gameName;
"""

"""
SELECT id, channel, name, gameName, pkgName, verCode, verName, filesize, downloadUrl, gameDesc, gameTypes,
        screenShotUrls, iconUrl, starNum, downloadCounts, gameLanguage, is_merge
        FROM crawler_info
        WHERE is_parse = 1
        and is_merge = 0
        ORDER BY name asc;


INSERT INTO iplay_game_pkg_info(game_id, market_channel, game_name, pkg_name, ver_code, ver_name, file_size,
        download_url, game_desc, game_types, downloaded_cnts, game_language, screen_shot_urls, icon_url, save_timestamp)
        VALUES (%(game_id)s, %(market_channel)s, %(game_name)s, %(pkg_name)s, %(ver_code)s, %(ver_name)s, %(file_size)s,
        %(download_urls)s, %(game_desc)s, %(game_types)s, %(downloaded_cnts)s, %(game_language)s, %(screen_shot_urls)s
        , %(icon_url)s, %(now)s)
        ON DUPLICATE KEY UPDATE
        game_id = VALUES(game_id),
        market_channel = VALUES(market_channel),
        game_name = VALUES(game_name),
        pkg_name = VALUES(pkg_name),
        ver_code = VALUES(ver_code),
        ver_name = VALUES(ver_name),
        file_size = VALUES(file_size),
        download_url = VALUES(download_url),
        game_desc = VALUES(game_desc),
        game_types = VALUES(game_types),
        downloaded_cnts = VALUES(downloaded_cnts),
        game_language = VALUES(game_language),
        screen_shot_urls = VALUES(screen_shot_urls),
        icon_url = VALUES(icon_url),
        update_timestamp = VALUES(save_timestamp)


select
    count(pkgName) as cnt
    , id
    , channel
    , name
    , gameName
    , pkgName
    , verCode
    , verName
    , filesize
    , downloadUrl
    , gameDesc
    , gameTypes
    , screenShotUrls
    , iconUrl
    , starNum
    , downloadCounts
    , gameLanguage
    , is_merge
    , min_sdk_version
    , game_tags
    , id_in_channel
    FROM crawler_info
    group by pkgName
    having cnt=1
    and pkgName != null
    or pkgName != ""
    order by gameName
    # limit 0, 1000


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
        ) ON DUPLICATE KEY UPDATE
        game_id = VALUES(game_id),
        market_channel = VALUES(market_channel),
        game_name = VALUES(game_name),
        pkg_name = VALUES(pkg_name),
        ver_code = VALUES(ver_code),
        ver_name = VALUES(ver_name),
        file_size = VALUES(file_size),
        download_url = VALUES(download_url),
        game_desc = VALUES(game_desc),
        game_types = VALUES(game_types),
        downloaded_cnts = VALUES(downloaded_cnts),
        game_language = VALUES(game_language),
        screen_shot_urls = VALUES(screen_shot_urls),
        icon_url = VALUES(icon_url),
        min_sdk = VALUES(min_sdk),
        update_timestamp = VALUES(save_timestamp)

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
        ) ON DUPLICATE KEY UPDATE
        game_name = VALUES(game_name),
        game_types = VALUES(game_types),
        screen_shot_urls = VALUES(screen_shot_urls),
        icon_url = VALUES(icon_url),
        detail_desc = VALUES(detail_desc),
        star_num = VALUES(star_num),
        download_counts = VALUES(download_counts),
        game_language = VALUES(game_language),
        update_timestamp = VALUES(save_timestamp)
"""
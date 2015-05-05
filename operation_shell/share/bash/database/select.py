# This file is part of database
# eew

from mysql_client import connections
from logs import logger


def get_gg_apk_info():
    gg_apk_info = {} # {game_id: {pkg_name:,game_name:,ver_code:,ver_name}}
    conn = connections("GGCursor")
    cursor = conn.cursor()
    sql = """
    SELECT pkg_name, game_name, ver_code, ver_name, game_id FROM
    iplay_game_pkg_info WHERE source=4 AND is_max_version=1 AND enabled=1
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_gg_apk_info error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    for row in rows:
        pkg_name = row[0]
        game_name = row[1]
        ver_code = int(row[2])
        ver_name = row[3]
        game_id = row[4]
        info = {
            'pkg_name': pkg_name,
            'game_name': game_name,
            'ver_code': ver_code,
            'ver_name': ver_name
        }
        gg_apk_info[game_id] = info
    return gg_apk_info


def get_gg_need_check_data():
    conn = connections("GGCursor")
    cursor = conn.cursor()
    sql = """
    SELECT game_id, detail_url FROM iplay_game_label_info WHERE source=4 AND
    enabled=1
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_gg_need_check_data error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_uc_apk_info():
    uc_apk_info = {} # {pkg_name: {game_name:,ver_code:,ver_name}}
    conn = connections("UCApkInfoCursor")
    cursor = conn.cursor()
    sql = """
    SELECT pkg_name, label, ver_code, ver_name FROM uc_apk_info WHERE data_source=4
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_uc_apk_info error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    for row in rows:
        pkg_name = row[0]
        game_name = row[1]
        ver_code = int(row[2])
        ver_name = row[3]
        info = {
            "game_name": game_name,
            "ver_code": ver_code,
            "ver_name": ver_name
        }
        uc_apk_info[pkg_name] = info
    return uc_apk_info


def get_appmarket_need_check_data():
    conn = connections("AppMarketCursor")
    cursor = conn.cursor()
    sql = """
    SELECT pkg_name, detail_url, apk_id, label FROM app_info WHERE enabled=1
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_appmarket_need_check_data error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return rows


def get_appmarket_apk_info():
    appmarket_apk_info = {} # {apk_id: {pkg_name:,ver_code:,ver_name:}}
    conn = connections("AppMarketCursor")
    cursor = conn.cursor()
    sql = """
    SELECT pkg_name, ver_code, ver_name, id FROM
    apk_info WHERE enabled=1
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_appmarket_apk_info error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    for row in rows:
        pkg_name = row[0]
        ver_code = int(row[1])
        ver_name = row[2]
        apk_id = row[3]
        info = {
            'pkg_name': pkg_name,
            'ver_code': ver_code,
            'ver_name': ver_name
        }
        appmarket_apk_info[apk_id] = info
    return appmarket_apk_info


def get_game_developer():
    """
    get developers. return .csv
    """
    conn = connections("GGCursor")
    cursor = conn.cursor()
    sql = """
    SELECT developer FROM iplay_game_developer
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_game_developer error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    with open('developer.csv', 'w') as files:
        for row in rows:
            developer = row[0]
            files.write('%s\n' % developer)

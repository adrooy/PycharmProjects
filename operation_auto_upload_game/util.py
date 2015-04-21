#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: utils.py
Author: limingdong
Date: 6/24/14
Description: 
"""

import os
import hashlib
from database.mysql_client import connections
from logs import logger


def is_dict_none(info):
    """
    判断字典的value值是否为空
    :param info:
    :return:
    """
    flag = True
    if isinstance(info, dict):
        for k, v in info.iteritems():
            if v and v != str(0):
                flag = False
            if not v and (k == "version_code" or k == "star_num" or k == "install_num" or k == "size"):
                info[k] = str(0)
    return flag


def show_dict(info):
    if isinstance(info, dict):
        for k, v in info.iteritems():
            print k
            print v
            print


def format_file_size(size):
    """
    将M, MB, mb, KB, GB, G换算成byte
    :param size:
    """
    result = 0
    num = filter(lambda ch: ch in '0123456789.', size)
    if size:
        if 'M' in size or 'm' in size or 'MB' in size or 'mb' in size:
            result = float(num) * 1024 * 1024
        elif 'KB' in size or 'kb' in size or 'K' in size or 'k' in size:
            result = float(num) * 1024
        elif 'GB' in size or 'gb' in size or 'G' in size or 'g' in size:
            result = float(num) * 1024 * 1024 * 1024
    return str(int(result) or '0')


def format_install_num(number):
    """
    将千，万，十万，百万，千万，亿换算成数字
    :param number:
    """

    result = 0
    num = filter(lambda ch: ch in '0123456789.', number)
    if num:
        num = float(num)
    if number:
        if u"小于" in number and u"千" in number:
            result = num * 1000
        elif u"千万" in number:
            result = num * 10000000
        elif u"百万" in number:
            result = num * 1000000
        elif u"十万" in number:
            result = num * 100000
        elif u"万" in number:
            result = num * 10000
        elif u"亿" in number:
            result = num * 100000000
        else:
            result = num

    return str(int(result) or '0')


def format_star_num(star, multi=1):
    result = 0
    num = filter(lambda ch: ch in '0123456789.', star)
    if num:
        num = float(num)
    if star:
        if u"分" in star:
            result = num * 10 * multi
        else:
            result = num * 10 * multi

    return str(int(result) or '0')


def format_android_level(level):
    # print level
    # 默认api_level 0
    if not level:
        return 0

    result = 0
    api_level = {
        "1.5": 3,
        "1.5.": 3,
        "1.6": 4,
        "1.6.": 4,
        "2.1": 7,
        "2.1.": 7,
        "2.2": 8,
        "2.2.": 8,
        "2.3": 10,
        "2.3.3": 10,
        "2.3.3.": 10,
        "3.0": 11,
        "3.0.": 11,
        "3.1": 12,
        "3.1.": 12,
        "3.2": 13,
        "3.2.": 13,
        "4.0": 14,
        "4.0.3": 15,
        "4.1.2": 16,
        "4.2.2": 17,
        "4.3": 18,
        "4.3.": 18,
        "4.4": 19,
        "4.4.": 19,
    }
    num = filter(lambda ch: ch in '0123456789.', level)
    if num:
        result = api_level.get(num, 8)
    return result


def format_google_play_name(g_name):
    """
    格式化GooglePlay上游戏的名字
    :param g_name:
    """
    if not isinstance(g_name, unicode):
        g_name = unicode(g_name, "utf-8")
    if u"™" in g_name:
        g_name = g_name.replace(u"™", "")
    if ":" in g_name:
        g_name = g_name.split(":")[0]

    return g_name


def ver_name_to_int(ver_name, apk_id=0):
    if ver_name is None or len(ver_name) == 0:
        return 0
    try:
        nums = ver_name.split('.')
        num = int(nums[0]) * 1000000
        if len(nums) > 1:
            num += int(nums[1]) * 1000
        if len(nums) > 2:
            num += int(nums[2])
        return num
    except Exception as e:
        #print "invalid ver_name of %d: %s" % (apk_id, ver_name)
        return 0


def gen_label_info_id(game_name):
    """
    根据游戏名生成id,使用sha1,保留8位
    google_gamename_mapping.game_name(360)
    google_gamename_mapping.game_name(GG官方)
    :param game_name:
    """
    if isinstance(game_name, unicode):
        g_name = game_name.encode("utf-8")
    else:
        g_name = game_name
    return hashlib.sha1(g_name.lower()).hexdigest().lower()[:8]


def gen_pkg_info_id(id_in_channel, pkg_name, ver_name, channel, ver_code_by_gg):
    """
    根据 id_in_channel(pkg_name)$ver_name$channel,使用sha1,保留8位
    "豌豆荚", "应用宝", "安卓市场", "91", "拇指玩" 使用包名
    "360", "百度", "小米", "爱吾"用id
    :param id_in_channel:
    :param pkg_name:
    :param ver_name:
    :param channel:
    :param ver_code_by_gg: GG自带的ver_code
    :return:
    """
    # print type(channel), channel
    # print "pkg"
    #if channel in ("豌豆荚", "应用宝", "安卓市场", "91", "拇指玩", "google", "GG官方", "360"):
        #name = str("samsung")+str(pkg_name) + "$" + ver_name + "$" + channel
    name = str(pkg_name) + "$" + ver_name + "$" + channel + "$" + ver_code_by_gg
    #else:
    #    name = str(id_in_channel) + "$" + ver_name + "$" + channel
    return hashlib.sha1(name.lower()).hexdigest().lower()[:8]


def get_is_crack_apk(channel):
    """
    是否为破解版,0不是，1是
    "豌豆荚", "应用宝", "安卓市场", "91", "360", "百度", "小米" : 0
    "爱吾", "拇指玩": 1
    :param channel:
    :return:
    """
    is_crack_apk = 0
    if channel in ("爱吾", "拇指玩"):
        is_crack_apk = 1
    return is_crack_apk


def check_developer(developer):
    """
    检查新增游戏厂商是否在厂商列表内
    :param infos:
    """
    conn = connections('Cursor')
    cursor = conn.cursor()
    try:
        sql = """
        INSERT INTO iplay_game_developer(developer) VALUES("%s") ON DUPLICATE KEY UPDATE developer = VALUES(developer);""" % developer
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("insert_developer name: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def test():
    # dicts_one = {"a": "", "b": '', "c": ""}
    # print is_dict_none(dicts_one)
    dicts = {'category': '', 'display_name': None, 'introduction': None, 'icon_url': None, 'screenshot_url': '', 'developers': []}
    print is_dict_none(dicts)
    nums = "18.18 M"
    print format_file_size(nums)
    print format_install_num(u"1.1万")
    print format_install_num(u"125")
    print format_install_num(u"5百万")
    print format_install_num(u"小于1.1千")
    print format_install_num(u"1.1千万")
    print format_install_num(u"1.9亿")
    print format_android_level(u"android 1.5.x")
    print format_android_level(u"Android 2.2.x以上")
    print format_android_level(u"1.6及以上固件版本")
    print format_android_level(u"Android 2.3 以上")
    print format_android_level(u"Android2.3.3及以上")
    print format_android_level(u"")
    print format_star_num("3.36363636364", 2)
    print gen_label_info_id("OX控$1.0.0$小米应用商店")
    print gen_pkg_info_id(1212, "com.tt.t", "1212", "应用宝")
    print gen_pkg_info_id("1212", "com.tt.t", "1212", "360")

if __name__ == '__main__':

    #0 com.atme.wuzetian.qihoo 1.1.0 360
    #0 com.snailgame.panda.qihoo360 1.1.0 360

    #print gen_pkg_info_id('0', 'com.square_enix.android_googleplay.dq8', '1.0.1', 'GG官方')
    print gen_label_info_id('自由之战(360)')
    #check_developer('腾讯')
    # test()
    # print format_game_name("Dot-Ranger")
    pass

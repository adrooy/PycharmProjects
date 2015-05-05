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


def gen_label_info_id(game_name, channel):
    """
    :param game_name:
    :param channel:
    :return:
    """
    g_name = '%s(%s)' % (game_name, channel)
    return hashlib.sha1(g_name.lower()).hexdigest().lower()[:8]


def gen_pkg_info_id(pkg_name, ver_name, channel, ver_code_by_gg):
    """
    :param pkg_name:
    :param ver_name:
    :param channel:
    :param ver_code_by_gg:  GG自带的ver_code 不存在任何相同的
    :return:
    """
    name = pkg_name + "$" + ver_name + "$" + channel + "$" + ver_code_by_gg
    return hashlib.sha1(name.lower()).hexdigest().lower()[:8]


def gen_image_name(url):
    """
    根据图片的下载地址生成图片名
    :param url:
    :return:
    """
    return hashlib.md5(url).hexdigest().lower()


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


if __name__ == '__main__':
    game_name = 'Slotomania - slot machines'
    pkg_name = 'air.com.playtika.slotomania'
    ver_name = '1.70.1'
    game_id = '07f4078a'
    apk_id = '194de4c7'
    channelid = '1'
    channel = 'GG官方'
    ver_code_by_gg = '1504281241'
    print gen_label_info_id(game_name, channel)
    print game_id
    print gen_pkg_info_id(pkg_name, ver_name, channel, ver_code_by_gg)
    print apk_id 

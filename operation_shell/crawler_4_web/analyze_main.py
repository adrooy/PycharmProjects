#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: analyze_main.py
Author: limingdong
Date: 7/28/14
Description: 
"""

import qihoo360, baidu, yingyongbao, xiaomi, hiapk, apk91, wandoujia, wandoujia_url
from logs import logger


def do_default_stuff(channel, name, html=''):
    print "do_default_stuff"
    logger.info("no found game(%s) on channel(%s)" % (name, channel))


def execute(cid, channel, html):
    choose = {
        "360": qihoo360.analyze,
        "91": apk91.analyze,
        "安卓市场": hiapk.analyze,
        "小米": xiaomi.analyze,
        "应用宝": yingyongbao.analyze,
        "百度": baidu.analyze,
        "豌豆荚": wandoujia_url.analyze,
    }
    info = choose.get(channel, do_default_stuff)(cid, str(html))
    return info


def get_id_from_url(channel, url):
    result = "0"
    if not url:
        return result

    if channel == "百度":
        urls = url.split("item?")
        if len(urls) == 2:
            params = urls[1].split("&")
            for param in params:
                if "docid=" in param:
                    result = param.replace("docid=", "")
                    break
    elif channel == "360":
        urls = url.split("soft_id/")
        if len(urls) == 2:
            result = urls[1]
    elif channel == "91":  # 91 获取包名
        urls = url.split("Android/")
        if len(urls) == 2:
            urls = urls[1].split("-")
            if len(urls) > 0:
                result = urls[0]
    elif channel == "小米":
        urls = url.split("detail/")
        if len(urls) == 2:
            result = urls[1]

    if channel != "安卓市场" and channel != "应用宝" and channel != "豌豆荚" and channel != "拇指玩" and result == "0":
        logger.debug("url4details get id error. URL: %s", url)
    return result


def format_game_name(game_name):
    """
    去掉各个渠道的名称
    :param game_name:
    :return:
    """
    if not game_name:
        return game_name
    if not isinstance(game_name, unicode):
        game_name = unicode(game_name, 'utf-8')
    game_name = game_name.replace(' ', '')
    if u"--小米版" in game_name:
        game_name = game_name.replace(u"--小米版", "")
    elif u"-小米版" in game_name:
        game_name = game_name.replace(u"-小米版", "")
    elif u"(小米版)" in game_name:
        game_name = game_name.replace(u"(小米版)", "")
    elif u"小米版" in game_name:
        game_name = game_name.replace(u"小米版", "")
    if u"(360专版)" in game_name:
        game_name = game_name.replace(u"(360专版)", "")
    elif u"360专版" in game_name:
        game_name = game_name.replace(u"360专版", "")
    elif u"360版" in game_name:
        game_name = game_name.replace(u"360版", "")
    if u"(91版)" in game_name:
        game_name = game_name.replace(u"(91版)", "")
    elif u"91版" in game_name:
        game_name = game_name.replace(u"91版", "")
    if u"百度版" in game_name:
        game_name = game_name.replace(u"百度版", "")
    if u"多酷版" in game_name:
        game_name = game_name.replace(u"多酷版", "")
    return game_name


def main(channel, html, url4details):
    info = dict()
    print 'start main'
    try:
        info = execute(0, channel, html)
        print '23'
    except Exception as e:
        logger.debug("analyze error. channel(%s),ERROR: %s" % (channel, str(e.args)))
        raise e
    return info


if __name__ == '__main__':
    main('', '', '')
    print "end"


#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: qihoo360.py
Author: limingdong
Date: 7/10/14
Description: 
"""


import re
import json
import utils
from BeautifulSoup import BeautifulSoup
from database.select import get_crawler_info


def get_basic_info(html_info):

    """
    获取游戏的基本信息
    :param html_info:
    :return: dict
    """
    result = {}

    html = html_info

    if html:
        screenshot_url = ""
        introduction = ""
        soup = BeautifulSoup(html)
        display_name = soup.find("span", {"class": "title"}).text
        icon_url = soup.find("div", {"class": "app-icon"}).find('img')['src']
        for img in soup.find("div", {"class": "overview"}).findAll('img'):
            src = img['src']
            screenshot_url += src + "\n"
        try:
            developers = soup.find("span", {"class": "dev-sites"}).text
        except:
            developers = ''
            #developers = soup.find("a", {"class": "dev-sites"}).span.text
        for div in soup.findAll("div", {"class": "con"}):
            introduction += div.text
        result["display_name"] = display_name
        result["introduction"] = introduction
        result["screenshot_url"] = screenshot_url
        result["developers"] = developers
        result["icon_url"] = icon_url
        print result

    return result


def analyze(c_id, html):
    basic_info = {}
    if html:
        basic_info = get_basic_info(html)

        if not utils.is_dict_none(basic_info):
            basic_info["is_parse"] = 1
        else:
            basic_info["is_parse"] = -1
        basic_info["c_id"] = c_id
    return basic_info


if __name__ == '__main__':
    # test()
    # n = "刀塔传奇"
    n = "100个任务10..."
    # n = "开心酷跑"
    c = "360"
    h = get_crawler_info(c, n)
    # print h[0]
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

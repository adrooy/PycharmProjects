#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: yingyongbao.py
Author: limingdong
Date: 7/10/14
Description: 
"""


import re
import utils
import json
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
        soup = BeautifulSoup(html)
        name = soup.find("div", {"class": "det-name-int"})
        detail = soup.find("div", {"class": "det-app-data-info"})
        app_tags = soup.find(id="J_DetCate")
        icon_info = soup.find("div", {"class": "det-icon"})
        screenshot_info = soup.findAll("div", {"class": "pic-img-box"})
        developers_info = soup.findAll("div", {"class": "det-othinfo-data"})
        # download_info = soup.find("a", {"class": "det-down-btn"})
        params_size = soup.find("div", {"class": "det-size"})
        # params_download_num = soup.find("div", {"class": "det-ins-num"})
        version_info = soup.find("div", {"class": "det-othinfo-data"})
        star = soup.find("div", {"class": "com-blue-star-num"})

        display_name = ""
        introduction = ""
        screenshot_url = ""
        category = ""
        pname = ""
        download = ""
        install_num = ""
        language = ""
        size = ""
        version = ""
        version_code = ""
        star_num = ""
        icon_url = ""
        developers = ""

        # 获取显示名
        if name:
            display_name = name.text
            if "v" in display_name:
                display_name = display_name.split("v")[0]

        # 获取简介
        if detail:
            introduction = detail.text

        # 获取标签类型信息
        if app_tags:
            category = app_tags.text

        # 获取icon
        if icon_info:
            icon_info = icon_info.find('img')
            icon_url = icon_info['src']

        # 获取截图url
        if screenshot_info:
            for screen in screenshot_info:
                img = screen.find('img')
                src = img['data-src']
                if src:
                    screenshot_url += src + "\n"

        if developers_info:
            developers = developers_info[len(developers_info)-1].text

        #获取下载地址,版本,安装数和大小
        if params_size:
            size = params_size.text
        if version_info:
            version = version_info.text.replace("V", "")
        if star:
            star_num = star.text

        #获取script游戏包名和下载地址
        script_infos = soup.findAll('script')
        for script in script_infos:
            pkg_infos = script.text
            if "var appDetailData = {" in pkg_infos:
                # print pkg_infos
                search = re.search(r"{([\s\S]*)}", pkg_infos, re.M | re.I)
                # print search.group()
                if search:
                    data = search.group()
                    data = data.replace("orgame", '"orgame"', 1)
                    data = data.replace("apkName", '"apkName"', 1)
                    data = data.replace("apkCode", '"apkCode"', 1)
                    data = data.replace("appId", '"appId"', 1)
                    data = data.replace("appName", '"appName"', 1)
                    data = data.replace("iconUrl", '"iconUrl"', 1)
                    data = data.replace("appScore", '"appScore"', 1)
                    data = data.replace("downTimes", '"downTimes"', 1)
                    data = data.replace("downUrl", '"downUrl"', 1)
                    data = data.replace("tipsUpDown", '"tipsUpDown"', 1)
                    pkg = json.loads(data)
                    download = pkg["downUrl"]
                    pname = pkg["apkName"]
                    install_num = pkg["downTimes"]
                    version_code = pkg['apkCode']

        result["display_name"] = display_name
        result["introduction"] = introduction
        result["screenshot_url"] = screenshot_url
        result["developers"] = developers
        result["category"] = category
        result["icon_url"] = icon_url
        result["version"] = version
        result["pkg_name"] = pname
        result["url1"] = download
        result["language"] = language
        result["version_code"] = version_code
        result["install_num"] = utils.format_install_num(install_num)
        result["size"] = utils.format_file_size(size)
        result["star_num"] = utils.format_star_num(star_num, 2)
        result["min_sdk_version"] = 0

    return result


def analyze(c_id, html):
    basic_info = {}
    if html:
        basic_info = get_basic_info(html)
        # utils.show_dict(basic_info)
        if not utils.is_dict_none(basic_info):
            basic_info["is_parse"] = 1
        else:
            basic_info["is_parse"] = -1
        basic_info["c_id"] = c_id
    return basic_info


if __name__ == '__main__':
    # n = "刀塔传奇"
    # n = "我爱猜动画片"
    # n = "欢乐斗地主(QQ游戏官方版)"
    n = "极限单车"
    c = "应用宝"
    h = get_crawler_info(c, n)
    # print h[0]
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: baidu.py
Author: limingdong
Date: 7/10/14
Description:
获取不到：
语言
评分
开发者
"""


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
        developers = ""
        category = ""
        pname = ""
        download = ""
        install_num = ""
        version = ""
        size = 0
        api_level = ""
        icon_url = ""

        soup = BeautifulSoup(html)
        display_name = soup.find("h1", {"class": "app-name"})
        introduction = soup.find("div", {"class": "brief-long"})
        short_desc = soup.find("span", {"class": "head-content"})
        app_tags = soup.find("div", {"class": "nav"})
        screenshot_info = soup.find("div", {"class": "section-body"})
        star_percent = soup.find("span", {"class": "star-percent"})
        params_download_num = soup.find("span", {"class": "download-num"})
        params_platform = soup.find("span", {"class": "params-platform"})
        data_info = soup.find("a", {"class": "inst-btn-big highspeed"})

        if data_info:
            download = data_info["data_url"]
            data_size = data_info["data_size"]
            data_ver_name = data_info["data_versionname"]
            # data_ver_code = data_info["data_versioncode"]
            data_pkg_name = data_info["data_package"]
            icon_url = data_info["data_icon"]

            size = data_size or 0
            version = data_ver_name
            # version_code = data_ver_code or 0
            pname = data_pkg_name

        # 获取显示名
        if display_name:
            display_name = display_name.text

        # 获取简介
        if introduction:
            # print introduction
            introduction = str(introduction).replace("<br />", "$##$")
            introduction = BeautifulSoup(introduction)
            introduction = introduction.text.replace("$##$", "\n")
            introduction = introduction.replace(u"收起", "")

        # 获取标签类型信息
        if app_tags:
            tags_text = app_tags.text
            if tags_text:
                category = tags_text.split("&gt;")[1]

        # 获取截图url
        if screenshot_info:
            for img in screenshot_info.findAll('img'):
                src = img['src']
                if src:
                    screenshot_url += src + "\n"

        #获取下载地址,版本,安装数和大小
        # if download_info:
        #     download = download_info["href"]
        if params_download_num:
            install_num = params_download_num.text
        if params_platform:
            api_level = params_platform.text

        # 获取评分
        if star_percent:
            star_percent = star_percent.get("style")

        # 获取简短描述
        if short_desc:
            short_desc = short_desc.text

        result["display_name"] = display_name
        result["introduction"] = introduction
        result["screenshot_url"] = screenshot_url
        result["developers"] = developers
        result["category"] = category
        result["icon_url"] = icon_url
        result["pkg_name"] = pname
        result["version"] = version
        result["url1"] = download
        result["language"] = ""
        result["version_code"] = 0
        result["install_num"] = utils.format_install_num(install_num)
        result["size"] = size
        result["min_sdk_version"] = utils.format_android_level(api_level)
        result["star_num"] = utils.format_star_num(star_percent)
        result["short_desc"] = short_desc or ""

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
    # n = "捕鱼达人2"
    n = "天天挂机"
    c = "百度"
    h = get_crawler_info(c, n)
    # print h[0]
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: hiapk.py
Author: limingdong
Date: 7/10/14
Description: 
"""


import re
import utils
from BeautifulSoup import BeautifulSoup
from database.select import get_crawler_info


def get_basic_info(html_info):
    result = {}

    html = html_info
    pname = ""
    download = ""
    install_num = ""
    language = ""
    version = ""
    size = ""
    display_name = ""
    category = ""
    icon_url = ""
    star_num = ""
    screenshot_url = ""
    api_level = ""

    if html:
        soup = BeautifulSoup(html)

        #获取下载地址,版本,安装数和大小
        app_version = soup.find(id="appSoftName")
        details = soup.find("div", {"class": "code_box_border"})
        introduction = soup.find(id="softIntroduce")
        screenshot_info = soup.find(id="screenImgUl")
        icon_star = soup.find("div", {"class": "detail_content"})

        if app_version:
            version = app_version.text
            if "(" in version:
                display_name = version.split("(")[0]
            search = re.search(r"\(.*\)", version, re.M | re.I)
            version = search.group().replace("(", "").replace(")", "")

        if details:
            spans = details.findAll("span", {"class": "font14"})
            for i, span in enumerate(spans):
                if i == 1:
                    install_num = span.text
                    if install_num:
                        install_num = install_num.replace(u"热度", "")
                if i == 3:
                    size = span.text
                if i == 4:
                    category = span.text
                if i == 6:
                    language = span.text

            # api_level = details.find("span", {"class": "font14 d_gj_line left"})
            api_level = details.find("span", {"class": "font14 detailMiniSdk d_gj_line left"})
            if api_level:
                    api_level = api_level.text

            download_info = details.find("a", {"class": "link_btn"})
            if download_info:
                download = download_info['href']
                if "appdown" in download:
                    pname_info = download.split("/")
                    download = "http://apk.hiapk.com" + download
                    if len(pname_info) > 2:
                        pname = pname_info[2].split("?")[0]

        if icon_star:
            icon = icon_star.find("img")
            star = icon_star.find("div", attrs={"class": re.compile(r"star_bg  star_m")})
            if icon:
                icon_url = icon['src']
            if star:
                if star:
                    star_num = star['class']

        if screenshot_info:
            screenshot_info = screenshot_info.findAll('img')
            for img in screenshot_info:
                src = img['src']
                if src:
                    screenshot_url += src + "\n"

        if introduction:
            # print introduction
            introduction = introduction.text

        result["pkg_name"] = pname
        result["version"] = version
        result["url1"] = download
        result["language"] = language
        result["display_name"] = display_name
        result["introduction"] = introduction
        result["screenshot_url"] = screenshot_url
        result["developers"] = ""
        result["category"] = category
        result["icon_url"] = icon_url
        result["version_code"] = ""
        result["install_num"] = utils.format_install_num(install_num)
        result["size"] = utils.format_file_size(size)
        result["star_num"] = utils.format_star_num(star_num, 0.2)
        result["min_sdk_version"] = utils.format_android_level(api_level)
        result["short_desc"] = ""

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
    # n = "雷神2：黑暗世界"
    # n = "2048方块"
    n = "100暗格"
    c = "安卓市场"
    h = get_crawler_info(c, n)
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

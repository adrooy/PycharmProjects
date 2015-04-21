#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: apk91.py
Author: limingdong
Date: 7/10/14
Description: 
"""


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
    introduction = ""
    api_level = ""

    if html:
        soup = BeautifulSoup(html)
        # print soup
        short_desc = soup.find("meta", {"name": "description"})
        #获取下载地址,版本,安装数和大小
        download_info = soup.find("a", {"class": "s_btn s_btn4"})
        details = soup.find("ul", {"class": "s_info"})
        name = soup.find("h1", {"class": "ff f20 fb fl"})
        introduction_info = soup.find("div", {"class": "o-content"})
        screenshot_info = soup.find(id="lstImges")
        icon_star = soup.find("div", {"class": "s_intro_pic fl"})

        screenshot_url = ""
        developers = ""
        category = ""
        icon_url = ""
        star_num = ""

        if download_info:
            download_info = download_info["href"]
            if download_info:
                download = "http://apk.91.com" + download_info
        if details:
            list_li = details.findAll("li")
            for i, li in enumerate(list_li):
                if i == 0:
                    version = li.text.replace(u"版本：", "").replace(u"历史版本", "")
                if i == 1:
                    install_num = li.text.replace(u"下载次数：", "")
                if i == 2:
                    size = li.text.replace(u"文件大小：", "")
                if i == 3:
                    api_level = li.text
                if i == 8:
                    if li:
                        developers = li.text.replace(u"开发商：", "")
                if i == 9:
                    if li:
                        tags = li.findAll("a")
                        for tag in tags:
                            category += tag.text + "\n"
        if icon_star:
            icon = icon_star.find('img')
            star = icon_star.find('a')
            if icon:
                icon_url = icon['src']
            if star:
                star_num = star['class']

        if introduction_info:
            introduction = introduction_info.text

        if name:
            display_name = name.text

        if screenshot_info:
            for img in screenshot_info.findAll('img'):
                src = img['src']
                if src:
                    screenshot_url += src + u"\n"

        result["pkg_name"] = pname
        result["version"] = version
        result["url1"] = download
        result["language"] = language
        result["display_name"] = display_name
        result["introduction"] = introduction
        result["screenshot_url"] = screenshot_url
        result["developers"] = developers
        result["category"] = category
        result["icon_url"] = icon_url
        result["version_code"] = ""
        result["install_num"] = utils.format_install_num(install_num)
        result["size"] = utils.format_file_size(size)
        result["star_num"] = utils.format_star_num(star_num, 2)
        result["min_sdk_version"] = utils.format_android_level(api_level)
        result["short_desc"] = short_desc.get("content")

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
    # n = "刀塔传奇"
    # n = "疯狂糖果消除"
    n = "100扇门"
    c = "91"
    h = get_crawler_info(c, n)
    # print h[0]
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

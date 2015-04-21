#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: xiaomi.py
Author: limingdong
Date: 7/10/14
Description: 
"""


import utils
import re
from BeautifulSoup import BeautifulSoup
from database.select import get_crawler_info


def get_basic_info(html_info):
    result = {}

    html = html_info
    pname = ""
    download = ""
    language = ""
    version = ""
    size = ""
    display_name = ""
    developer = ""
    category = ""
    icon_url = ""
    star_num = ""
    screenshot_url = ""
    introduction = ""

    if html:
        soup = BeautifulSoup(html)

        #获取下载地址,版本,安装数和大小
        app_info = soup.find("div", {"class": "app-info"})
        download_info = soup.find("a", {"class": "download"})
        details = soup.find("div", {"class": "details preventDefault"})
        introductions = soup.find("p", {"class": "pslide"})
        screenshot_info = soup.find(id="J_thumbnail_wrap")

        if download_info and "http://app.mi.com" not in download_info:
            download = "http://app.mi.com" + download_info['href']

        if details:
            list_li = details.find("ul").findAll("li")
            for index, element in enumerate(list_li):
                if index == 1:
                    size = element.text
                if index == 3:
                    version = element.text
                if index == 7:
                    pname = element.text

        if app_info:
            name = app_info.find("h3")
            icon = app_info.find("img")
            categorys = app_info.find("p", {"class": "special-font action"})
            developers = app_info.findAll("p")
            star = app_info.find("div", attrs={"class": re.compile(r"star1-hover")})
            if name:
                display_name = name.text
            if icon:
                icon_url = icon['src']
            if categorys:
                category = categorys.text
                if "|" in category:
                    category = category.split("|")
                    category = category[0].replace(u"分类：", "")
            if developers:
                if len(developers) == 2:
                    d = developers[0]
                    developer = d.text
            if star:
                star_nums = star['class']
                nums = star_nums.split('-', 2)
                if len(nums) == 3:
                    star_num = nums[2]

        if screenshot_info:
            screenshot_info = screenshot_info.findAll('img')
            for img in screenshot_info:
                src = img['src']
                if src:
                    screenshot_url += src + "\n"

        if introductions:
            introductions = str(introductions).replace("<br />", "$##$")
            introductions = BeautifulSoup(introductions)
            introduction = introductions.text.replace("$##$", "\n")

        result["pkg_name"] = pname
        result["version"] = version
        result["url1"] = download
        result["language"] = language
        result["display_name"] = display_name
        result["introduction"] = introduction
        result["screenshot_url"] = screenshot_url
        result["developers"] = developer
        result["category"] = category
        result["icon_url"] = icon_url
        result["version_code"] = ""
        result["install_num"] = ""
        result["size"] = utils.format_file_size(size)
        result["star_num"] = utils.format_star_num(star_num)
        result["min_sdk_version"] = 0
        result["short_desc"] = ""

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
    n = "2048"
    # n = "刀塔传奇"
    c = "小米"
    h = get_crawler_info(c, n)
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

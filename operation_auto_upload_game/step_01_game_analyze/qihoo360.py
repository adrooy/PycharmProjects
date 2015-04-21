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
        soup = BeautifulSoup(html)
        display_name = soup.find(id="app-name")
        introduction = soup.find(id="html-brief")
        app_tags = soup.find("div", {"class": "app-tags"})
        icon_url = soup.find("dt")
        short_desc = soup.find("dl", {"class": "clearfix"})

        screenshot_url = ""
        developers = ""
        category = ""
        pname = ""
        download = ""
        install_num = ""
        language = ""
        version_name = ""
        version_code = 0
        size = 0
        star_num = 0
        min_sdk_version = 0

        # 获取显示名
        if display_name:
            display_name = display_name.find("span").text

        # 如果获取不到介绍信息，尝试第二种方式
        if not introduction:
            introduction = soup.find("div", {"class": "infors"})

        # 获取简介，截图，开发商和类型
        if introduction:

            # 获取截图url
            scroll = introduction.find(id="scrollbar")
            desc = introduction.find("div", {"class": "breif"})
            if scroll:
                imgs = scroll["data-snaps"]
                for img in imgs.split(","):
                    if img and "icon.png" not in img:
                        screenshot_url += img + "\n"
            else:
                for img in introduction.findAll("img"):
                    src = img['src']
                    if src and "icon.png" not in src:
                        screenshot_url += src + "\n"

            if desc:
                desc_str = str(desc).replace("<br />", "$##$")
                desc_str = desc_str.replace("</td>", "$##$</td>")
                desc_str = BeautifulSoup(desc_str)
                introduction = desc_str.text.replace("$##$", "\n").replace("&nbsp;", " ")
                introduction = introduction.replace("versioncode", "\nversioncode")
                introduction = introduction.replace("updatetime", "\nupdatetime")
            else:
                introduction = str(introduction).replace("<br />", "$##$")
                introduction = introduction.replace("</td>", "$##$</td>")
                introduction = introduction.replace("</p>", "$##$</p>")
                introduction = BeautifulSoup(introduction)
                introduction = introduction.text.replace("$##$", "\n").replace("&nbsp;", " ")
                introduction = introduction.replace("versioncode", "\nversioncode")
                introduction = introduction.replace("updatetime", "\nupdatetime")

        #获取游戏包名和下载地址
        script_infos = soup.findAll('script')
        for script in script_infos:
            pkg_infos = script.text
            if "var detail = (function () {" in pkg_infos:
                search = re.search(r"return {([\s\S]*)};", pkg_infos, re.M | re.I)
                # print search
                if search:
                    data = search.group().replace("return", "").replace(";", "").replace("'", "\"")
                    pkg = json.loads(data)
                    pname = pkg['pname']
                    download = pkg['downloadUrl']
                    version_code = pkg['vcode']

        #获取语言，版本,安装数和大小
        pf = soup.find("div", {"class": "pf"})
        basic_info = soup.find("div", {"class": "base-info"})

        if pf:
            pf_s3 = pf.findAll("span", {"class": "s-3"})  # 下载量
            star = pf.find("span", {"class": "s-1 js-votepanel"})  # 评分
            if len(pf_s3) == 2:
                install_num = pf_s3[0].text
                size = pf_s3[1].text
                install_num = install_num.replace(u"下载：", "").replace(u"次", "")
            if star:
                star_num = star.text

        if basic_info:
            infos = basic_info.findAll("td")
            for info in infos:
                text = info.text
                # print text
                if u"作者：" in text:
                    developers = text.replace(u"作者：", "")
                if u"语言" in text:
                    language = text.replace(u"语言：", "")
                if u"版本" in text:
                    search = text.split("versioncode")
                    if len(search) > 0:
                        version_name = search[0].replace(u"版本：", "")
                if u"系统：" in text:
                    min_sdk_version = utils.format_android_level(text)

        # 获取标签类型信息
        if app_tags:
            tags = app_tags.findAll("a")
            for tag in tags:
                if "360" in tag.text:
                    continue
                category += tag.text + "\n"

        if icon_url:
            icon_url = icon_url.find("img")
            icon_url = icon_url["src"]

        # 获取简短描述
        if short_desc:
            short_desc = short_desc.find("p")
            if short_desc:
                short_desc = short_desc.text
                short_desc = short_desc.replace(u"【小编点评】", "")

        result["display_name"] = display_name
        result["introduction"] = introduction
        result["screenshot_url"] = screenshot_url
        result["developers"] = developers
        result["category"] = category
        result["icon_url"] = icon_url
        result["pkg_name"] = pname
        result["version"] = version_name
        result["url1"] = download
        result["language"] = language
        result["version_code"] = version_code
        result["install_num"] = utils.format_install_num(install_num)
        result["size"] = utils.format_file_size(size)
        result["star_num"] = utils.format_star_num(star_num)
        result["min_sdk_version"] = min_sdk_version
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
    # n = "刀塔传奇"
    n = "100个任务10..."
    # n = "开心酷跑"
    c = "360"
    h = get_crawler_info(c, n)
    # print h[0]
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

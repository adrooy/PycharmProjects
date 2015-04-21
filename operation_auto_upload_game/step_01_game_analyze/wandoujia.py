#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: download_lists.py
Author: limingdong
Date: 7/29/14
Description:
"""

import utils
from database.select import get_crawler_info


def get_basic_info(html_json):
    result = {}
    d = eval(html_json)
    apk_dict = d.get("apks")[0]

    pkg_name = apk_dict["packageName"]
    game_name = d["title"]
    ver_name = apk_dict["versionName"]
    language = apk_dict["language"]
    filesize = apk_dict["bytes"]
    download_url = apk_dict["downloadUrl"]
    ver_code = apk_dict["versionCode"]
    min_sdk = apk_dict["minSdkVersion"]

    description = d["description"]
    icons = d["icons"]
    icon_url = icons.get("px256")
    if not icon_url:
        icon_url = icons.get("px100")
    elif not icon_url:
        icon_url = icons.get("px78")
    elif not icon_url:
        icon_url = icons.get("px68")
    elif not icon_url:
        icon_url = icons.get("px48")

    screenshots = ""
    screenshots_info = d["screenshots"]
    if screenshots_info:
        if "normal" in screenshots_info:
            screenshots = "\n".join(screenshots_info["normal"])
        elif "small" in screenshots_info:
            screenshots = "\n".join(screenshots_info["small"])

    installed_count = d["installedCount"]

    categories = ""
    for cate in d["categories"]:
        categories += cate["name"] + "\n"
    tags = ""
    for tag in d["tags"]:
        tags += tag["tag"] + "\n"
    developer = d["developer"]
    title = d["title"]
    if title:
        title = title.replace("<em>", "").replace("</em>", "")
        title = title.replace(" ", "")
        game_name = title

    star = d["likesRate"] or 0
    dev = developer["name"]

    result["pkg_name"] = pkg_name
    result["version"] = ver_name
    result["url1"] = download_url["url"]
    result["language"] = '\n'.join(language)
    result["display_name"] = game_name
    result["introduction"] = description.replace("<br />", "\n")
    result["screenshot_url"] = screenshots
    result["developers"] = dev
    result["category"] = tags
    result["icon_url"] = icon_url
    result["version_code"] = ver_code
    result["install_num"] = installed_count
    result["size"] = filesize
    result["star_num"] = star
    result["min_sdk_version"] = min_sdk
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
    n = "坚守阵地"
    c = "豌豆荚"
    h = get_crawler_info(c, n)
    info = analyze(0, h[0])
    utils.show_dict(info)
    print "end"

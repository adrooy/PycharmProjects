#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: download_images.py
Author: limingdong
Date: 8/15/14
Description:
下载google play 游戏icon和截图
"""


import os
import sys
import hashlib
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(BASE_DIR)
import requests
from database import select


#http_proxy = "192.168.1.240:3128"
#https_proxy = "192.168.1.240:3128"
http_proxy = "http://23.92.25.62.3128"
https_proxy = "http://23.92.25.62:3128"
proxyDict = {
    "http": http_proxy,
    "https": https_proxy,
}


def mk_dir(game_id):
    path = os.path.abspath(os.path.dirname(__file__))
    icon_path = os.path.join(path, "image", game_id, "icon")
    screen_path = os.path.join(path, "image", game_id, "screen")
    if not os.path.exists(icon_path):
        os.makedirs(icon_path)
    if not os.path.exists(screen_path):
        os.makedirs(screen_path)
    return icon_path, screen_path


def download_image(info):
    game_id = info["game_id"]
    icon_url = info["icon_url"]
    screen_shot_urls = info["screen_shot_urls"]

    if "ggpht.com" not in icon_url and "googleusercontent.com" not in icon_url:
        return
    if "https:" not in icon_url:
        icon_url = icon_url.replace("http:", "https:")

    icon_path, screen_path = mk_dir(game_id)
    # 下载icon
    request_url(icon_url, icon_path)
    # 下载截图
    for screen_url in screen_shot_urls.split("\n"):
        if "https:" not in screen_url:
            screen_url = screen_url.replace("http:", "https:")
        request_url(screen_url, screen_path)


def request_url(url, path):
    if not url or not path:
        return
    if not ("http" in url):
        return
    image_name = gen_image_name(url)
    file_list = os.listdir(path)
    # 文件存在,不存入

    for f in file_list:
        if image_name in f:
            return
    #print image_name
    # 下载文件
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0',
        'Referer': 'https://play.google.com/store/apps/category/GAME',
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip',  # 以gzip下载html，降低网络资源负荷
        'Accept-Language': 'zh-cn,en-us;q=0.7,en;q=0.3',
        'Content-Length': '86',
        'Cookie': 'PREF=ID=54d3e46c668f74ce:U=0806b1988518afdd:TM=1411874099:LM=1416486632:S=qv9drTd2LIVCahAX; NID=67=J6fg2e3bnpbDdaN_xcMZXrH7E-VvzYuXKf4jLz-oLWCJ-O_xEzG9JQ2nng236XgOwpm3DCq0JL6m_RIveJM4ASXqy8-7xkuEI-CK4Gz_Imbr3Wt9I8iUvuaf3GwH7pCD; _ga=GA1.3.86026158.1413180514; _gat=1; PLAY_PREFS=CgJVUxD2z9aCnSkosra56Zwp:S:ANO1ljJYk5JjleSs',
        'Host': 'play.google.com',
    }
    r = requests.get(url, stream=True, proxies=proxyDict, verify=False)
    content_type = r.headers.get('content-type')

    name = os.path.join(path, "%s.webp" % image_name)
    if content_type:
        suffix = content_type.split("/")[1]
        name = os.path.join(path, "%s.%s" % (image_name, suffix))

    # 如果不是图片格式记录
    if not "image" in content_type:
        logger.debug("file: %s is not webp,is %s", name, content_type)

    if r.status_code == 200:
        with open(name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def gen_image_name(url):
    """
    根据图片的下载地址生成图片名
    :param url:
    :return:
    """
    return hashlib.md5(url).hexdigest().lower()


def main(game_id):
    infos = select.get_google_pkg_info(game_id)
    for info in infos:
        download_image(info)


if __name__ == "__main__":
    main()





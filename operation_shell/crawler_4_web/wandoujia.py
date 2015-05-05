#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: qihoo360.py
Author: limingdong
Date: 7/10/14
Description: 
"""


from BeautifulSoup import BeautifulSoup


def analyze(html):

    """
    获取游戏的基本信息
    :param html_info:
    :return: dict
    """
    result = {}
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
        for div in soup.findAll("div", {"class": "con"}):
            introduction += div.text
        result["game_name"] = display_name
        result["detail_desc"] = introduction
        result["screen_shot_urls"] = screenshot_url
        result["developer"] = developers
        result["icon_url"] = icon_url
    return result

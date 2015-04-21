#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: analyze_game_data.py
Author: limingdong
Date: 7/30/14
Description:
分析游戏信息,生成label和pkg表.
1.先分析包名相同的信息,
2.再根据游戏名对游戏进行分类.

label表图片地址尽量不使用百度的.
"""

import utils
import time
import game_name_format

from game_types import game_type


def prepare_pkg_info(info, apk_info, channel):
    """
    准备pkg_info的数据, is_crack_apk:是否为破解版，0不是，1是.
    :param info:
    """
    pkg_info = dict()
    if info:
        pkg_info["market_channel"] = channel
        pkg_info["game_name"] = info["display_name"]
        pkg_info["pkg_name"] = apk_info["pkg_name"]
        pkg_info["ver_code"] = apk_info["ver_code"]
        pkg_info["ver_name"] = apk_info["ver_name"]
        pkg_info["file_size"] = apk_info["file_size"]
        pkg_info["download_urls"] = apk_info["baidupan_url"]
        desc = info["introduction"]
        if desc:
            desc = desc.replace("<br />", "\n").replace("&nbsp;", " ")
        pkg_info["game_desc"] = desc
        pkg_info["game_types"] = ''
        pkg_info["origin_types"] = ''
        pkg_info["downloaded_cnts"] = 0
        pkg_info["game_language"] = ''
        pkg_info["screen_shot_urls"] = info["screenshot_url"]
        pkg_info["icon_url"] = info["icon_url"]
        pkg_info["now"] = str(int(time.time()))
        pkg_info["is_crack_apk"] = 0
        if "ggvercode" not in apk_info:
            apk_info["ggvercode"] = "null"
        apk_id = utils.gen_pkg_info_id(0, apk_info["pkg_name"], apk_info["ver_name"], channel, apk_info["ggvercode"])
        pkg_info["apk_id"] = apk_id
        pkg_info["min_sdk_version"] = apk_info["min_sdk"]
        pkg_info["url4details"] = apk_info["detail_url"]
        pkg_info["gpu_vender"] = apk_info["gpu_vender"]
    return pkg_info


def gen_label_and_pkg_info(info, apk_info, channel):
    """
    生成label和pkg的信息,
    label游戏名需要处理
    pkg不需要
    :param info:
    :return:
    """
    label_info = dict()  # game_label_info表准备数据
    pkg_info = dict()  # game_pkg_info表准备数据
    g_name = game_name_format.format_label_game_name(info['display_name'])  # 处理游戏名
    if g_name:
        game_id = apk_info['gameid']
        pkg_info = prepare_pkg_info(info, apk_info, channel)
        screen = info['screenshot_url']
        icon = info['icon_url']
        detail = info['introduction']
        developers = info['developers']

        if detail and "<br />" in detail:
            detail = detail.replace("<br />", "\n")
        if detail and "&nbsp;" in detail:
            detail = detail.replace("&nbsp;", " ")

        pkg_info["game_id"] = game_id
        pkg_info["ver_name"] = apk_info['ver_name']
        pkg_info["ver_code"] = apk_info['ver_code']
        pkg_info["signature_md5"] = apk_info['signature_md5']
        pkg_info["file_md5"] = apk_info['file_md5']
        pkg_info["update_desc"] = apk_info['update_desc']
        pkg_info["ver_code_by_gg"] = apk_info['ggvercode']

        label_info["game_id"] = game_id
        label_info["ver_name"] = apk_info['ver_name']
        label_info["short_desc"] = ''
        label_info["game_name"] = g_name
        label_info["display_name"] = g_name
        label_info["star_num"] = 0
        label_info["download_counts"] = 0
        label_info["game_types"] = ''
        label_info["origin_types"] = ''
        label_info["screen_shot_urls"] = screen
        label_info["icon_url"] = icon
        label_info["detail_desc"] = detail
        label_info["game_language"] = ''
        label_info["file_size"] = apk_info["file_size"]
        label_info["developer"] = developers
        label_info["now"] = str(int(time.time()))
    return label_info, pkg_info


def main(infos, apk_info, channel):
    """
    生成label_info, pkg_infos
    """
    label_info, pkg_info = gen_label_and_pkg_info(infos, apk_info, channel)
    return label_info, pkg_info


if __name__ == '__main__':
    info = {'category': '\xe6\x89\x91\xe5\x85\x8b\xe6\xa3\x8b\xe7\x89\x8c\n\xe4\xbc\x91\xe9\x97\xb2\xe6\x97\xb6\xe9\x97\xb4\n\xe5\xbe\xb7\xe5\xb7\x9e\xe6\x89\x91\xe5\x85\x8b\n\xe7\x9b\x8a\xe6\x99\xba\n\xe4\xbc\x91\xe9\x97\xb2\xe7\x9b\x8a\xe6\x99\xba\n\xe6\xa3\x8b\xe7\x89\x8c\n', 'star_num': 71, 'display_name': u'\u53e3\u888b\u5fb7\u5dde\u6251\u514b', 'language': '', 'install_num': 1368537, 'introduction': '- \xe5\xba\x94\xe7\x94\xa8\xe5\xb8\x82\xe5\x9c\xba\xe5\xa2\x9e\xe9\x95\xbf\xe6\x9c\x80\xe5\xbf\xab\xe7\x9a\x84\xe5\xbe\xb7\xe5\xb7\x9e\xe6\x89\x91\xe5\x85\x8bAPP\n- \xe9\x9a\x8f\xe6\x97\xb6\xe9\x9a\x8f\xe5\x9c\xb0\xe5\x8f\xaf\xe4\xbb\xa5\xe8\xbf\x9e\xe5\x85\xa5\xe7\x9a\x84\xe6\x8e\x8c\xe4\xb8\x8a\xe5\xbe\xb7\xe5\xb7\x9e\xe6\x89\x91\xe5\x85\x8b\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8\n- \xe9\xa3\x8e\xe9\x9d\xa1\xe5\x85\xa8\xe7\x90\x83\xe7\x9a\x84\xe7\xbb\x8f\xe5\x85\xb8\xe6\x89\x91\xe5\x85\x8b\xe6\xb8\xb8\xe6\x88\x8f\n\xe5\xa6\x82\xe6\x9e\x9c\xe4\xbd\xa0\xe7\x83\xad\xe7\x88\xb1\xe5\xbe\xb7\xe5\xb7\x9e\xe6\x89\x91\xe5\x85\x8b\xef\xbc\x8c\xe8\xb5\xb6\xe5\xbf\xab\xe5\x8a\xa0\xe5\x85\xa5\xe5\x8f\xa3\xe8\xa2\x8b\xe5\xbe\xb7\xe5\xb7\x9e\xe6\x89\x91\xe5\x85\x8b\xe4\xbf\xb1\xe4\xb9\x90\xe9\x83\xa8\xe5\x90\xa7\xef\xbc\x81\n\xe8\xbf\x99\xe6\x98\xaf\xe5\x85\xa8\xe4\xb8\x96\xe7\x95\x8c\xe6\x9c\x80\xe6\xb5\x81\xe8\xa1\x8c\xe7\x9a\x84\xe5\x85\xac\xe5\x85\xb1\xe7\x89\x8c\xe6\x89\x91\xe5\x85\x8b\xe6\xb8\xb8\xe6\x88\x8f\xe3\x80\x82\n\xe5\xbe\xb7\xe5\xb7\x9e\xe6\x89\x91\xe5\x85\x8b\xe6\x98\xaf\xe6\x9c\x80\xe5\x85\xb7\xe4\xbd\x8d\xe7\xbd\xae\xe6\x80\xa7\xe7\x9a\x84\xe6\x89\x91\xe5\x85\x8b\xe8\xa1\x8d\xe7\x94\x9f\xe6\xb8\xb8\xe6\x88\x8f\xe4\xb9\x8b\xe4\xb8\x80\xef\xbc\x8c\xe5\x9b\xa0\xe4\xb8\xba\xe6\x89\x80\xe6\x9c\x89\xe8\xbd\xae\xe6\x95\xb0\xe7\x9a\x84\xe4\xb8\x8b\xe6\xb3\xa8\xe6\xac\xa1\xe5\xba\x8f\xe7\xbb\xb4\xe6\x8c\x81\xe4\xb8\x8d\xe5\x8f\x98\xef\xbc\x8c\xe6\x98\xaf\xe7\xbe\x8e\xe5\x9b\xbd\xe5\xa4\xa7\xe5\xa4\x9a\xe6\x95\xb0\xe5\xa8\xb1\xe4\xb9\x90\xe5\x9c\xba\xe5\x86\x85\xe6\x9c\x80\xe5\x8f\x97\xe6\xac\xa2\xe8\xbf\x8e\xe7\x9a\x84\xe6\x89\x91\xe5\x85\x8b\xe8\xa1\x8d\xe7\x94\x9f\xe6\xb8\xb8\xe6\x88\x8f\xe3\x80\x82', 'icon_url': 'http://img.wdjimg.com/mms/icon/v1/6/88/3e5d127c94094a1054d6ecc7dba78886_256_256.png', 'c_id': 0, 'min_sdk_version': 8, 'version_code': 240, 'short_desc': '', 'version': '2.4.0', 'url1': 'http://apps.wandoujia.com/redirect?signature=52db113&url=http%3A%2F%2Fapk.wandoujia.com%2Fe%2F66%2F3d04621c1c9712cafd1ea435d5bd466e.apk&pn=com.poketec.texas&md5=3d04621c1c9712cafd1ea435d5bd466e&apkid=11114344&vc=240&size=8725413&pos=t/detail&tokenId=lbe&appType=GAME', 'screenshot_url': 'http://img.wdjimg.com/mms/screenshot/6/5a/f3876a6b9629d39c637b9214f4aa35a6_320_480.jpeg\nhttp://img.wdjimg.com/mms/screenshot/d/e2/5781b93a3443449a3950cf330457ee2d_320_480.jpeg\nhttp://img.wdjimg.com/mms/screenshot/3/56/3cfa23170d405cb6f2473e8a0485b563_320_480.jpeg\nhttp://img.wdjimg.com/mms/screenshot/b/04/c3c21c46f17b220dae771483cd24e04b_320_480.jpeg\nhttp://img.wdjimg.com/mms/screenshot/6/ff/aeb0fc68d88e8c211e828f031d15aff6_320_480.jpeg', 'pkg_name': 'com.poketec.texas', 'id_in_channel': '0', 'developers': '\xe6\xb7\xb1\xe5\x9c\xb3\xe5\x8f\xa3\xe8\xa2\x8b\xe7\xa7\x91\xe6\x8a\x80\xe6\x9c\x89\xe9\x99\x90\xe5\x85\xac\xe5\x8f\xb8', 'is_parse': 1, 'channel': '\xe8\xb1\x8c\xe8\xb1\x86\xe8\x8d\x9a', 'size': 8725413}
    label_info, pkg_info = main(info)
    print 'label, pkg'
    print label_info
    print pkg_info
    print "end"

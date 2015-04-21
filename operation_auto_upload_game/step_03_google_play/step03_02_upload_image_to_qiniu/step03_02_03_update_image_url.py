#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: upload_images.py
Author: limingdong
Date: 8/15/14
Description: 
"""

import os

from logs import logger
from database.mysql_client import connections
from step_03_google_play.db import select_google_pkg_info


cur_dir = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(cur_dir, "image")
host = "http://7mnmgb.com1.z0.glb.clouddn.com/"
icon_host = "http://7mnmgb.com1.z0.glb.clouddn.com/%s?imageView/1/w/180/h/180"


def update_label_and_pkg_img(info):
    conn = connections('RemoteCursor')
    cursor = conn.cursor()
    print info
    try:
        label_sql = """
            UPDATE iplay_game_label_info
            SET screen_shot_urls = %(screen_shot_urls)s
            , icon_url = %(icon_url)s
            where game_id = %(game_id)s;
        """
        pkg_sql = """
            UPDATE iplay_game_pkg_info
            SET screen_shot_urls = %(screen_shot_urls)s
            , icon_url = %(icon_url)s
            where game_id = %(game_id)s;
        """
        cursor.execute(label_sql, info)
        cursor.execute(pkg_sql, info)
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.debug("update_label_and_pkg_img: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute():
    for lists in os.listdir(image_path):
        update_info = dict()
        game_id = lists

        updated_ids = []
        infos = select_google_pkg_info()
        for info in infos:
            updated_ids.append(info["game_id"])
        # game_id 不在需要更新的列表中,不执行更新操作
        if game_id not in updated_ids:
            continue
        path = os.path.join(image_path, game_id)
        if os.path.isdir(path):
            icon_path = os.path.join(path, "icon")
            screen_path = os.path.join(path, "screen")
            icons = os.listdir(icon_path)
            screens = os.listdir(screen_path)

            update_info["game_id"] = game_id
            update_info["icon_url"] = "\n".join([icon_host % url.split(".")[0] for url in icons])
            update_info["screen_shot_urls"] = "\n".join([host + url.split(".")[0] for url in screens])

            if update_info:
                update_label_and_pkg_img(update_info)
                print "update game_id : %s success." % game_id


if __name__ == "__main__":
    execute()

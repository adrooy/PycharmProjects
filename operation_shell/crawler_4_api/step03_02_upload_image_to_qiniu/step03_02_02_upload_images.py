#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: upload_images.py
Author: limingdong
Date: 8/15/14
Description:
上传图片到七牛云存储
"""


import os
import hashlib
import qiniu.conf
import qiniu.io
import qiniu.rs

qiniu.conf.ACCESS_KEY = "RvYl39IQUBtJiz-i18sZFsxIym_qfYbArHQ8f_PI"
qiniu.conf.SECRET_KEY = "B7tipfdcF_FlUhiO8JowDn5cHujYWrBPhxjdin_i"

bucket_name = "ggfile"
policy = qiniu.rs.PutPolicy(bucket_name)  # 空间名即bucket_name
uptoken = policy.token()

cur_dir = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(cur_dir, "image")
#print "image_path"
#print image_path


def upload(path, name):
    """
    上传图片的路径和图片名
    :param path: 图片的路径
    :param name: 图片名
    """
    local_file = os.path.join(path, name)
    print  '\n'
    print name,path
    key, suffix = name.split(".")

    # 如果图片名存在,则不继续上传
    image_ids = read_file("uploaded_image_ids.txt")
    if key in image_ids:
        return
    else:
        write_file(key, "uploaded_image_ids.txt")

    extra = qiniu.io.PutExtra()
    extra.mime_type = "image/%s" % suffix
    ret, err = qiniu.io.put_file(uptoken, key, local_file, extra)


def write_file(content, filename):
    uploaded_game_ids = os.path.join(cur_dir, filename)
    with open(uploaded_game_ids, "ab+") as data:
        data.read()
        data.write(content+"\n")
        data.close()


def read_file(filename):
    uploaded_game_ids = os.path.join(cur_dir, filename)
    with open(uploaded_game_ids, "r") as data:
        content = data.read()
        data.close()
    return content


def file_md5(path, name):
    local_file = os.path.join(path, name)
    return hashlib.md5(open(local_file).read()).hexdigest()


def execute():
    for lists in os.listdir(image_path):
        game_id = lists
    #    game_ids = read_file("uploaded_game_ids.txt")
    #    if game_id in game_ids:
    #        continue

        path = os.path.join(image_path, game_id)
        if os.path.isdir(path):
            icon_path = os.path.join(path, "icon")
            screen_path = os.path.join(path, "screen")
            icons = os.listdir(icon_path)
            screens = os.listdir(screen_path)
            for icon in icons:
                upload(icon_path, icon)
                # pass
            for screen in screens:
                upload(screen_path, screen)
            write_file(game_id, "uploaded_game_ids.txt")
        print "uploaded game_id : %s image success." % game_id


def clean_common_image():
    """
    清理相同的图片,以计算图片的md5值为准
    """
    for lists in os.listdir(image_path):
        game_id = lists
        path = os.path.join(image_path, game_id)
        # print
        # print game_id
        md5_dict = dict()
        if os.path.isdir(path):
            screen_path = os.path.join(path, "screen")
            screens = os.listdir(screen_path)
            for screen in screens:
                md5 = file_md5(screen_path, screen)
                if md5 in md5_dict:
                    md5_dict[md5] = md5_dict[md5] + "$#$" + screen
                else:
                    md5_dict[md5] = screen
            for key, value in md5_dict.iteritems():
                # print key, value
                if "$#$" in value:
                    for index, image in enumerate(value.split("$#$")):
                        if index == 0:
                            continue
                        # 移除图片
                        remove_image_path = os.path.join(screen_path, image)
                        logger.info("remove image index:%d, path: %s", index, remove_image_path)
                        os.remove(remove_image_path)
                        # print index, remove_image_path
            # print "================================"


def main():
    print 'start upload_image'
    try:
        clean_common_image()
        execute()
    except:
        print "error"

if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: main.py
Author: limingdong
Date: 9/24/14
Description: 用于自动上传apk信息
"""


import time
import urllib
import hashlib
import urllib2
import sys
import requests
#sys.path.append('/home/mgmt/operation_auto_upload_apk')
#print sys.path
import utils
from browser import browser
from logs import logger
from step_01_game_analyze import analyze_main
from step_02_crawler_info_analyze import analyze_game_data
from step_03_google_play import step_03_01_search_by_pkg_name as google
from step_03_google_play.step03_02_upload_image_to_qiniu import step03_02_01_download_images
from step_03_google_play.step03_02_upload_image_to_qiniu import step03_02_02_upload_images
from step_03_google_play.step03_02_upload_image_to_qiniu import step03_02_03_update_image_url
#from step_04_game_analyze import analyze_main
#from step_04_crawler_info_analyze import analyze_game_data

def gen_wdj_url(pkg_name):
    """
    生成豌豆荚的url
    :param pkg_name: 分类
    :return:
    """
    host = "http://api.wandoujia.com/v1/apps/%s" % pkg_name

    auth = "lbe"
    key = "03ff2ad5a1ea48968bfda5c3c18bf2cf"
    timestamp = int(time.time() * 100)
    timestamp = bytes(timestamp)

    md5 = hashlib.md5()
    md5.update(auth + key + timestamp)
    token = md5.hexdigest()
    # print token

    params = {
        'id': auth,
        'timestamp': timestamp,
        'token': token,
    }
    encodeurl = urllib.urlencode(params)
    url = host + "?" + encodeurl
    return url


def get_data_wdj(web_url):
    """
    获取豌豆荚信息
    :return:
    """
    result = ""
    try:
        content = urllib2.urlopen(web_url, timeout=10)
        result = content.read()
        result = result.replace("false", "False")
        result = result.replace("null", "None")
    except Exception as e:
        raise e

    return str(result)


def get_data(page_url, referer):
    info = ''
    try:
        page = browser.read(page_url, referer)
        # 91,360...被封时
        if "很抱歉..." in page:
            info = 'ERROR:已被91封禁,等段时间在试'
        elif '<?xml version="1.0" encoding="UTF-8"?>' in page:
            info = 'ERROR:获取页面失败,请查看url是否正确'
        elif page and page.strip():
            info = page
    except Exception as e:
        # raise e
        logger.debug("get_data ERROR: %s", str(e.args))
    return info


def google_apk(apk_info, channel, detail_url):
    try:
    #if 1==1:
        # 1.入库google游戏
        google.main(apk_info, channel, detail_url)
        time.sleep(5)
    except Exception as e:
        logger.debug("upload_data入库google游戏 ERROR: %s", str(e.args))
        return 301
    try:
#    if 1==1:
        # 2.下载图片
        step03_02_01_download_images.main()
        time.sleep(5)
    except Exception as e:  
        logger.debug("upload_data下载图片 ERROR: %s", str(e.args))
        return 302
    try:
        # 3.上传图片
        step03_02_02_upload_images.main()
        time.sleep(5)
    except Exception as e:
        logger.debug("upload_data上传图片 ERROR: %s", str(e.args))
        return 303
    try:
        # 4.更新图片
        step03_02_03_update_image_url.execute()
        time.sleep(5)
    except Exception as e:
        logger.debug("upload_data更新图片 ERROR: %s", str(e.args))
        return 304
    return 399


def popularize_apk(apk_info, channel, detail_url):
    apk_info['detail_url'] = detail_url
    try:
    #if 1==1:
        if 'http://www.wandoujia.com' in detail_url:
    #        pkg_name = apk_info['pkg_name']
    #        url = gen_wdj_url(pkg_name)
    #        html = get_data_wdj(url)
            html = get_data(detail_url, detail_url)
            info_channel = '豌豆荚'
    except Exception as e:
        logger.debug("upload_data get_data ERROR: %s", str(e.args))
        return 101
    try:
    #if 1==1:
        # 2.获取分析后的信息
        info = analyze_main.main(info_channel, html, detail_url)
    except Exception as e:
        logger.debug("upload_data获取分析后的信息 ERROR: %s", str(e.args))
        return 102
    try:
    #if 1==1:
        # 3.根据生成的信息获取label和pkg信息
        label_info, pkg_info = analyze_game_data.main(info, apk_info, channel)
        label_info['source'] = 4
        pkg_info['source'] = 4
        pkg_info['save_user'] = apk_info['save_user']
        pkg_info['ver_name'] = pkg_info['ver_name']
        label_info['save_user'] = apk_info['save_user']
    except Exception as e:
        logger.debug("upload_data生成的信息获取label和pkg信息 ERROR: %s", str(e.args))
        return 103
   # print '\n'
   # for key,value in pkg_info.items():
   #      print key,value
   # print '\n'
   # for key,value in label_info.items():
   #      print key,value
   # print '\n'
   # sys.exit()
    print pkg_info['game_name']
    print label_info['game_name']
    print pkg_info['apk_id']
    utils.check_developer(label_info["developer"])
    try:
        insert.insert_label_info(label_info)
        insert.insert_pkg_info(pkg_info)
    except Exception as e:
        logger.debug("upload_data插入数据 ERROR: %s", str(e.args))
        return 104
    return 199


def other_apk(apk_info, channel, detail_url):
    try:
        # 1.获取json或者html信息
        if channel == "豌豆荚":
            pkg_name = apk_info['pkg_name']
            url = gen_wdj_url(pkg_name)
            html = get_data_wdj(url)
        else:
            html = get_data(detail_url, detail_url)
    except Exception as e:
        logger.debug("upload_data get_data ERROR: %s", str(e.args))
        return 101
    try:
        # 2.获取分析后的信息
        info = analyze_main.main(channel, html, detail_url)
        # 如果下载地址都为空,则提示错误.如果有百度盘地址,则选用百度盘地址
    except Exception as e:
        logger.debug("upload_data获取分析后的信息 ERROR: %s", str(e.args))
        return 102
    try:
        # 3.根据生成的信息获取label和pkg信息
        label_info, pkg_info = analyze_game_data.main(info)
    except Exception as e:
        logger.debug("upload_data生成的信息获取label和pkg信息 ERROR: %s", str(e.args))
        return 103
    try:
        # 4.插入数据,如果是百度盘的下载地址,先将其设为enabled=0
        if pkg_info["download_url_type"] == 2:
            # print pkg_info["game_id"]
            insert.update_pkg_by_game_id(pkg_info["game_id"])
        else:
            # 如果是渠道自己的下载地址,比较apk大小
            flag = apk_url_judge(pkg_info['file_size'], pkg_info['download_url'])
            if not flag:
                return 106
        insert.insert_label_info(label_info)
        insert.insert_pkg_info(pkg_info)
    except Exception as e:
        logger.debug("upload_data插入数据 ERROR: %s", str(e.args))
        return 104
    return 199


def baidupan_url_judge(file_size, url):
    """
    判断百度盘中文件大小和上传的是否一致
    :param file_size:
    :param url:
    """
    html = requests.post(url, timeout=10).content
    #html = get_data(url, url)
   # print html
    if str(file_size) in html:
        return True
    else:
        return False


def apk_url_judge(file_size, url):
    """
    判断国内其他渠道文件大小和上传的是否一致
    :param file_size:
    :param url:
    """
    html = browser.get_data_size(url, url)
    print html
   # print html
    if file_size == html:
        return True
    else:
        return False


def get_channel_info():
    """
    获取45上cgi返回的渠道信息
    """
    channel_info = {}
    cgi_url = "http://192.168.1.45:8000/cgi-bin/channels.py?original=0"
    content = urllib2.urlopen(cgi_url, timeout=10)
    result = content.read().split('\n')
    for item in result:
        try:
            channelid, channel = item.split(': ')
            channel_info[channelid] = channel
        except:
            pass
    cgi_url = "http://192.168.1.45:8000/cgi-bin/channels.py?original=1"
    content = urllib2.urlopen(cgi_url, timeout=10)
    result = content.read().split('\n')
    for item in result:
        try:
            channelid, channel = item.split(': ')
            channel_info[channelid] = channel
        except:
            pass
    return channel_info
 

def popularize(upload_id, save_user):
    """
    source = 4
    推广游戏入库
    """
    GPU = {
        '2': 2, #ADRENO
        '3': 3, #NVIDIA
        '4': 4, #POWERVR
        '5': 5, #MALI
        '52': 52, #ADRENO
        '53': 53, #NVIDIA
        '54': 54, #POWERVR
        '55': 55 #MALI
    }
    POPULARIZE = ['CMGE', '360', '其他']
    channel_dict = {
        '57': 'CMGE',
        '58': '360',
        '59': '其他'
    }
    msg = ""
    upload_game = dict()
    upload_game['id'] = upload_id

    try:
    #if 1==1:
        upload_iplay = select.get_iplay_upload_game(upload_id)
        #print upload_iplay
        apk_info = upload_iplay['apk_info']
        baidupan_url = upload_iplay['baidupan_url']

        apk_info = eval(apk_info)
        apk_info['save_user'] = save_user
        file_size = apk_info['file_size']
        #flag = True
        #if 'pan.baidu.com' in baidupan_url:
        flag = baidupan_url_judge(file_size, baidupan_url)
        if flag:
            channel = upload_iplay['channel']
            gpu_vender = 1
            if 'channelid' in apk_info:
                channel = channel_dict[apk_info['channelid']]
                gpu_vender = GPU[apk_info['channelid']] if apk_info['channelid'] in GPU else 1
            apk_info['gpu_vender'] = gpu_vender
            detail_url = upload_iplay['detail_url']
            ver_name = apk_info['ver_name']
            if ver_name:
                ver_name = filter(lambda ch: ch in '0123456789.', ver_name)
            try:
                if "ggvercode" not in apk_info:
                    apk_info["ggvercode"] = "null"
                apk_id = utils.gen_pkg_info_id(0, apk_info["pkg_name"], ver_name, channel, apk_info["ggvercode"])
            except Exception as e:
                logger.debug("upload_data ERROR: %s", str(e.args))
                apk_id = 0
                msg = 202
            upload_game['apk_id'] = apk_id
            print apk_info["pkg_name"], ver_name, channel
    #        if channel in GOOGLE_CHANNEL:
    #            upload_game['source'] = 3
    #            upload_game['channel'] = channel
    #            apk_info['baidupan_url'] = baidupan_url
    #            msg = google_apk(apk_info, channel, detail_url)
            if channel in POPULARIZE:
                upload_game['source'] = 4
                apk_info['baidupan_url'] = baidupan_url
                upload_game['game_id'] = apk_info["gameid"] 
                upload_game['channel'] = channel
                msg = popularize_apk(apk_info, channel, detail_url)
            upload_game['now'] = int(time.time())
            upload_game['is_finished'] = 1
            upload_game['msg'] = msg
            insert.update_iplay_upload_game(upload_game)
            print msg
        else:
            msg = 201
            upload_game['now'] = int(time.time())
            upload_game['is_finished'] = 1
            upload_game['msg'] = msg
            insert.update_iplay_upload_game_baidupan(upload_game)
    except Exception as e:
    #else:
        msg = 201
        upload_game['now'] = int(time.time())
        upload_game['is_finished'] = 1
        upload_game['msg'] = msg
        insert.update_iplay_upload_game_baidupan(upload_game)
    return msg


def main(upload_id, save_user):
    msg = ""
    upload_game = dict()
    upload_game['id'] = upload_id

    GOOGLE_CHANNEL = ['GG官方', '三星', '高通版', '英伟达', 'PowerVR', 'Mali', '汉化', '全球版', 'GG特色版', 'GG存档版', 'GG纪念版', 'GG官方原包', '三星原包', '高通版原包', '英伟达原包', 'PowerVR原包', 'Mali原包']
    #step_03_google_play/db.py 中的def select_google_pkg_info()　也得添加渠道用来筛选要抓取的图片
    
    CHANNEL = {
        '1': 'GG官方',
        '2': '高通版',
        '3': '英伟达',
        '4': 'PowerVR',
        '5': 'Mali',
        '6': '三星',
        '7': 'GG特色版',
        '8': 'GG存档版',
        '9': 'GG纪念版',
        '10': '汉化',
        '30': '全球版',
        '51': 'GG官方原包',
        '52': '高通版原包',
        '53': '英伟达原包',
        '54': 'PowerVR原包',
        '55': 'Mali原包',
        '56': '三星原包'
    }

    GPU = {
        '2': 2, #ADRENO
        '3': 3, #NVIDIA
        '4': 4, #POWERVR
        '5': 5, #MALI
        '52': 52, #ADRENO
        '53': 53, #NVIDIA
        '54': 54, #POWERVR
        '55': 55 #MALI
    }

    try:
    #if 1==1:
        upload_iplay = select.get_iplay_upload_game(upload_id)
        #print upload_iplay
        apk_info = upload_iplay['apk_info']
        baidupan_url = upload_iplay['baidupan_url']

        apk_info = eval(apk_info)
        apk_info['save_user'] = save_user
        file_size = apk_info['file_size']
        #flag = True
        #if 'pan.baidu.com' in baidupan_url:
        flag = baidupan_url_judge(file_size, baidupan_url)
        if flag:
            channel = upload_iplay['channel']
            gpu_vender = 1
            if 'channelid' in apk_info:
                channel = CHANNEL[apk_info['channelid']]
                gpu_vender = GPU[apk_info['channelid']] if apk_info['channelid'] in GPU else 1
            apk_info['gpu_vender'] = gpu_vender
            detail_url = upload_iplay['detail_url']
            ver_name = apk_info['ver_name']
            if ver_name:
                ver_name = filter(lambda ch: ch in '0123456789.', ver_name)
            try:
                if "ggvercode" not in apk_info:
                    apk_info["ggvercode"] = "null"
                if channel == "samsung":
                    market_channel = "三星"
                    apk_id = utils.gen_pkg_info_id(0, apk_info["pkg_name"], ver_name, market_channel, apk_info["ggvercode"])
                else:
                    apk_id = utils.gen_pkg_info_id(0, apk_info["pkg_name"], ver_name, channel, apk_info["ggvercode"])
            except Exception as e:
                logger.debug("upload_data ERROR: %s", str(e.args))
                apk_id = 0
                msg = 202
            print apk_id, 'upload'

            upload_game['apk_id'] = apk_id
            if channel in GOOGLE_CHANNEL:
            #if channel == 'GG官方' or channel == 'samsung':
                upload_game['source'] = 3
                upload_game['channel'] = channel
                apk_info['baidupan_url'] = baidupan_url
                upload_game['game_id'] = apk_info["gameid"] 
                msg = google_apk(apk_info, channel, detail_url)
            else:
                return 201
#            else:
#                upload_game['source'] = 1
#                apk_info['baidupan_url'] = baidupan_url
#                msg = other_apk(apk_info, channel, detail_url)
            upload_game['now'] = int(time.time())
            upload_game['is_finished'] = 1
            upload_game['msg'] = msg
            insert.update_iplay_upload_game(upload_game)
        else:
            msg = 201
            upload_game['now'] = int(time.time())
            upload_game['is_finished'] = 1
            upload_game['msg'] = msg
            insert.update_iplay_upload_game_baidupan(upload_game)
    except Exception as e:
    #else:
        msg = 201
        upload_game['now'] = int(time.time())
        upload_game['is_finished'] = 1
        upload_game['msg'] = msg
        insert.update_iplay_upload_game_baidupan(upload_game)

    return msg


if __name__ == '__main__':
    # import json
    # apk_info = json.loads(sys.argv[1])
    #msg = main(sys.argv[1])
    # msg = main(25)
    print sys.argv
    flag = sys.argv[1]
    if flag == '3':
        msg = main(sys.argv[2], sys.argv[3])
    if flag == '4':
        msg = popularize(sys.argv[2], sys.argv[3])
    print msg


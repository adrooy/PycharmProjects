#!/usr/bin/python
#-*- coding:utf-8 -*-


import os
import sys
import json
import time
import MySQLdb
import logging

DATE = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#TIME = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
LOGS_DIR = '/home/mgmt/update_52_iplay_data/log/update_52_iplay_data_%s.log' % DATE
file_handler = logging.FileHandler(LOGS_DIR)
file_handler.setLevel(logging.DEBUG)
#console_handler = logging.StreamHandler()
#console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
#console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
#logger.addHandler(console_handler)


def forum_data_conn(func):
    def conn(*args, **kwargs):
#        conn = MySQLdb.connect(host='192.168.1.45',port=3306,user='root',passwd='111111',db='forum',charset='utf8')
        conn = MySQLdb.connect(host='192.168.0.1',port=3306,user='forum',passwd='VQq*d@GY4F7J6]MP',db='forum',charset='utf8')
#        conn = MySQLdb.connect(host='localhost',port=3306,user='forum',passwd='VQq*d@GY4F7J6]MP',db='forum',charset='utf8')
        conn.ping(True)
        db = conn.cursor()
        result = func(db, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return conn

@forum_data_conn
def update_label(db, filename):
    with open(filename) as files:
        for line in files:
            labels = json.loads(line)
            delete_sql = ""
            insert_sql = ""
            game_ids = []
            games = []
            for label in labels:
                game_id = label[0]
                game_ids.append(tuple([game_id]))
                games.append(tuple(label))
            delete_sql = """
            DELETE FROM iplay_game_label_info WHERE game_id = %s;
            """
            db.executemany(delete_sql, game_ids)
            insert_sql = """
            INSERT INTO iplay_game_label_info(
            game_id
            , game_name
            , game_types
            , game_tags
            , screen_shot_urls
            , icon_url
            , forum_url
            , post_url
            , tid
            , short_desc
            , detail_desc
            , star_num
            , download_counts
            , game_language
            , save_timestamp
            , update_timestamp
            , min_apk_size
            , max_apk_size
            , min_ver_name
            , max_ver_name
            , source
            , enabled
            , display_name
            , is_changed
            , subscript
            , color_label
            , disable_reason
            , origin_types
            , game_alias
            , search_boost
            , forum_plugin_screen_urls
            , developer
            , category_id
            , gg_download_cnt
            , subscript_expire_time
            , is_in_test
            , gg_download_week
            , save_user 
            , update_user
            , detail_url
            , detail_desc_html
            , editor_desc_html
            ) VALUES (
            %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s);
            """
            db.executemany(insert_sql, games)

@forum_data_conn
def update_pkg(db, filename):
    with open(filename) as files:
        for line in files:
            pkgs = json.loads(line)
            delete_sql = ""
            insert_sql = ""
            apk_ids = []
            games = []
            for pkg in pkgs:
                apk_id = pkg[0]
                apk_ids.append(tuple([apk_id]))
                games.append(tuple(pkg))
            delete_sql = """
            DELETE FROM iplay_game_pkg_info WHERE apk_id = %s;
            """
            db.executemany(delete_sql, apk_ids)
            insert_sql = """
            INSERT INTO iplay_game_pkg_info(
            apk_id
            , game_id
            , market_channel
            , game_name
            , pkg_name
            , file_md5
            , ver_code
            , ver_name
            , signature_md5
            , file_size
            , download_url
            , forum_url
            , post_url
            , min_sdk
            , game_desc
            , game_types
            , game_tags
            , downloaded_cnts
            , is_crack_apk
            , tid
            , depend_google_play
            , game_language
            , save_timestamp
            , update_timestamp
            , screen_shot_urls
            , icon_url
            , is_max_version
            , download_url_type
            , enabled
            , source
            , is_plugin_required
            , is_changed
            , required_plugin_ids
            , url4details
            , disable_reason
            , origin_types
            , gg_download_cnt
            , gg_download_week
            , gpu_vender
            , ver_code_by_gg
            , update_desc
            , save_user
            , update_user
            , file_type
            ) VALUES(
            %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s
            , %s);
            """
            db.executemany(insert_sql, games)



def upload_file(url, file_msg, name='file', compress=None, timeout=None):
    if isinstance(file_msg, file):
        msg = file_msg.read()
    elif isinstance(file_msg, basestring):
        msg = file_msg
    else:
        raise
    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = list()
    data.append('--%s' % boundary)
    if compress:
        msg = compress(msg)
    data.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (name, 'filename'))
    data.append('Content-Type: %s\r\n' % 'text/plain')
    data.append(msg)
    data.append('--%s--\r\n' % boundary)

    body = '\r\n'.join(data)

    import urllib2
    req = urllib2.Request(url, data=body)
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
    if timeout:
        resp = urllib2.urlopen(req, timeout=timeout)
    else:
        resp = urllib2.urlopen(req)

    return resp


def handle_data(DIR, DATE):
    try:
        tar_file = os.path.join(DIR, '%s.tar.gz' % DATE)
        os.system("tar -zxvf %s -C %s" % (tar_file, DIR))
        logger.debug('success tar -zxvf data')
    except Exception as e:
        logger.debug('ERROR in update_52_iplay_data.py tar -zxvf data: %s' % str(e.args))
        return 101
    #DIR = os.path.join(os.getcwd(), 'data', DATE)
    DIR = os.path.join('/home/mgmt/update_52_iplay_data', DATE)
    for files in os.listdir(DIR):
        filename = os.path.join(DIR, files)
        if os.path.isfile(filename):
            if files.endswith('sql'):
                #logger.debug(filename)
                if filename.endswith('iplay_ad_info_%s.sql' % DATE):
                    try:
                        import zlib
                        url = 'http://123.59.55.206/api/v1/reload-ad-db?src=1'
                        resp = upload_file(url=url, file_msg=open(filename), compress=zlib.compress)
                        import json
                        if json.loads(resp.read())['result']['code'] != 0:
                            raise Exception('scp iplay_ad_info to 123.59.55.206 error')
                        logger.debug('success insert %s in 206' % filename)
                    except Exception as e:
                        logger.debug('ERROR in insert sql: %s 206' % str(e.args))
                        return 102
                try:
                    os.system("mysql -h192.168.0.1 -uforum -pVQq*d@GY4F7J6]MP forum < %s" % filename)
                    logger.debug('success insert %s ' % filename)
                except Exception as e:
                    logger.debug('ERROR in insert sql: %s' % str(e.args))
                    return 102
            if files.startswith('label'):
                try:
                    update_label(filename)
                    logger.debug('success insert %s ' % filename)
                except Exception as e:
                    logger.debug('ERROR in insert label: %s' % str(e.args))
                    return 103
            if files.startswith('pkg'):
                try:
                    update_pkg(filename)
                    logger.debug('success insert %s ' % filename)
                except Exception as e:
                    logger.debug('ERROR in insert pkg: %s' % str(e.args))
                    return 104
    try:
        os.system("sh /home/mgmt/operation/cmd/gen_service_mapping.sh")
        logger.debug('success insert sh gen_service_mapping.sh')
    except Exception as e:
        logger.debug('ERROR in update_52_iplay_data.py gen_service_mapping: %s' % str(e.args))
        return 105
    return 106

if __name__ == '__main__':      
    logger.debug('\n\n\n')
    logger.debug('START')
    try:
        DATE = sys.argv[1]
        DIR = '/home/mgmt/update_52_iplay_data/'
        result = handle_data(DIR, DATE)
        logger.debug('returns: %s' % (result))
        tar_file = os.path.join(DIR, '%s.tar.gz' % DATE)
        os.system("rm -rf  %s" % tar_file)
        tar_file = os.path.join(DIR, '%s' % DATE)
        os.system("rm -rf  %s" % tar_file)
        logger.debug('END')
        print result
    except Exception as e:
        logger.debug('ERROR in update_52_iplay_data.py main: %s' % str(e.args))

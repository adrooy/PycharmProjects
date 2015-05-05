#!/usr/bin/python

import os
import sys
import time
import json
import MySQLdb
import logging
import subprocess
import select
import signal


DATE = time.strftime('%Y-%m-%d', time.localtime(time.time()))
#TIME = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
LOGS_DIR = '/home/mgmt/update_52_iplay_data/log/update_52_iplay_data_%s.log' % DATE
file_handler = logging.FileHandler(LOGS_DIR)
file_handler.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def getDate(timeStamp):
    if timeStamp:
        timeArray = time.localtime(timeStamp)
        date = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
    else:
        date = ''
    return date

#mysqldump -hlocalhost -uforum -pVQq*d@GY4F7J6]MP forum iplay_topic_info > $PATH/$DATE/iplay_topic_info_$DATE.sql
def forum_data_conn(func):
    def conn(*args, **kwargs):
        conn = MySQLdb.connect(host='localhost',port=3306,user='forum',passwd='VQq*d@GY4F7J6]MP',db='forum',charset='utf8')
        conn.ping(True)
        db = conn.cursor()
        result = func(db, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return conn

@forum_data_conn
def get_label_data(db, PATH):
    pkgs = []
    labels = []
    game_ids = set()
    sql = """
    SELECT * FROM iplay_game_pkg_info
    WHERE source = 2 or source = 3
    or (source = 1 AND is_plugin_required = 1) 
    """
    db.execute(sql)
    pkgs = list(db.fetchall())
    for pkg in pkgs:
        game_ids.add(pkg[1])
    #print 'pkgs: ',len(pkgs)
    for game_id in game_ids:
        sql = """
        SELECT * FROM iplay_game_label_info WHERE game_id = "%s"
        """ % game_id
        db.execute(sql)
        label = db.fetchall()[0]
        if label:
            labels.append(label)
    DATE = getDate(time.time()).split(' ')[0]
    #print 'labels: ',len(labels)
    label_file = os.path.join(PATH, DATE, 'label_%s' % DATE)
    pkg_file =  os.path.join(PATH, DATE, 'pkg_%s' % DATE)
    with open(label_file, 'w') as files:
        files.write(json.dumps(labels))
    with open(pkg_file, 'w') as files:
        files.write(json.dumps(pkgs))

@forum_data_conn
def insert_iplay_release_list(db):
    sql = """
    INSERT INTO iplay_release_list(start_date, is_finished) VALUES(%s, %s)
    """ % (str(time.time()), '0')
    db.execute(sql)
    sql = """
    SELECT last_insert_id() FROM iplay_release_list;   
    """
    list_id = int(db.execute(sql))
    return list_id

@forum_data_conn
def update_iplay_release_list(db, list_id, msg):
    sql = """
    UPDATE iplay_release_list SET msg=%s, is_finished=1, end_date=%s WHERE id=%s
    """ % (msg, str(time.time()), list_id)
    #print sql
    db.execute(sql)

def release():
    result = 0
    try:
        os.system("sh /home/mgmt/operation/cmd/gen_service_mapping.sh >> %s 2>&1" % LOGS_DIR)
    except Exception as e:
        logger.debug('ERROR in release.py gen_service_mapping: %s' % str(e.args))
        return 201
    try:
        os.system("sh /home/mgmt/update_52_iplay_data/get_178_iplay_data.sh >> %s 2>&1" % LOGS_DIR)
        logger.debug("start update_52_data.sh")
        args = ['python', '/home/mgmt/update_52_iplay_data/update.py']
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        timeout = 400
        start = int(time.time())
        while 1:
            f = select.select([p.stdout], [], [], timeout)
            if p.stdout in f[0]:
                tmp = p.stdout.read()
                if tmp:
                    result = tmp
                    break
            else:
                result = 301
                break
    except Exception as e:
        logger.debug('ERROR in release.py get_178_iplay_data: %s' % str(e.args))
        return 202
    return result

if __name__ == '__main__':
    logger.debug('\n\n\n')
    logger.debug('START')
    try:
        list_id = sys.argv[1]
        msg = release()
        logger.debug('MSG: %s' % (msg))
        update_iplay_release_list(list_id, msg)
        logger.debug('END')
    except Exception as e:
        logger.debug('ERROR in release.py main: %s' % str(e.args))

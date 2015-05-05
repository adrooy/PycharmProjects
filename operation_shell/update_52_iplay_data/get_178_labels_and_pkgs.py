#!/usr/bin/python

import os
import sys
import time
import json
import MySQLdb
import logging

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
def get_labels_and_pkgs(db, PATH):
    pkgs = []
    labels = []
    game_ids = set()
    sql = """
    SELECT * FROM iplay_game_pkg_info
    WHERE source = 2 or source = 3 or source = 4
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
        if game_id == '04ec1944':
            print label[25]
    DATE = getDate(time.time()).split(' ')[0]
    #print 'labels: ',len(labels)
    label_file = os.path.join(PATH, DATE, 'label_%s' % DATE)
    pkg_file =  os.path.join(PATH, DATE, 'pkg_%s' % DATE)
    with open(label_file, 'w') as files:
        files.write(json.dumps(labels))
    with open(pkg_file, 'w') as files:
        files.write(json.dumps(pkgs))

if __name__ == '__main__':
    try:
        PATH = sys.argv[1]
        get_labels_and_pkgs(PATH)
    except Exception as e:
        logger.debug('ERROR in get_178_labels_and_pkgs.py main: %s' % str(e.args))

#!/usr/bin/python
#-*- coding: utf-8 -*-


import os
import subprocess
import MySQLdb
import MySQLdb.cursors
import commands  
from step_03_google_play.googleplay import GooglePlayAPI
from step_03_google_play.config import *
from jianfan import ftoj      
import logging


# 创建logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# 创建handler，用于写入文件
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_DIR = os.path.join(BASE_DIR, 'googleplay_gamename.log')
file_handler = logging.FileHandler(LOGS_DIR)
file_handler.setLevel(logging.DEBUG)
# 创建handler,用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
# 定义handler输出格式
formatter = logging.Formatter('%(asctime)-15s %(levelname)s %(message)s')
# formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

HOST = "192.168.0.1"
USER = "forum"
PWD = "VQq*d@GY4F7J6]MP"
DB = "forum"
PORT = 3306

OPTIONS = {
    "52Cursor": {
        "host": HOST,
        "user": USER,
        "passwd": PWD,
        "db": DB,
        "port": PORT,
        "charset": "utf8",
        "use_unicode": False,
        "cursorclass": MySQLdb.cursors.SSCursor,
    }
}


def connections(db_name):
    settings = OPTIONS.get(db_name)
    if not settings:
        raise Exception("the options is error")
    host = settings.get("host")
    user = settings.get("user")
    passwd = settings.get("passwd")
    db = settings.get("db")
    port = settings.get("port")
    charset = settings.get("charset")
    use_unicode = settings.get("use_unicode")
    cursorclass = settings.get("cursorclass")
    con = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset,
                          use_unicode=use_unicode, cursorclass=cursorclass)
    return con


def check_pkg_name():
    pkg_names = {} # { pkg_name : "" }
    conn = connections('52Cursor')
    cursor = conn.cursor()
    sql = "SELECT pkg_name FROM iplay_tool_gamename_mapping WHERE game_name IS NULL AND not_google_game IS NULL"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        pkg_name = row[0]
        pkg_names[pkg_name] = ""
    cursor.close()
    conn.commit()
    conn.close()
    return pkg_names


def handle_pkg_name(pkg_names):
    for pkg_name in pkg_names:
        shell = "ps -ef | grep python | grep %s | grep -v 'grep' | awk '{print $10}'" % pkg_name
        result = commands.getstatusoutput(shell)
        if pkg_name in result: #正在抓取游戏名
            pass 
        else: #抓取游戏名
            try: #gooleplay的游戏名插入数据库
                game_name = crawler(pkg_name)
                not_google_game = 0
            except: #不时googleplay的加上标记not_google_game=1
                not_google_game = 1
                game_name = ""
        conn = connections('52Cursor')
        cursor = conn.cursor()
        if not_google_game:
            sql = '''UPDATE iplay_tool_gamename_mapping SET not_google_game=1 WHERE pkg_name = "%s"''' % pkg_name
        else:
            sql = '''UPDATE iplay_tool_gamename_mapping SET game_name="%s" WHERE pkg_name = "%s"''' % (game_name, pkg_name)
        logger.debug(sql)
        cursor.execute(sql)
        cursor.close()
        conn.commit()
        conn.close()


def login():
    api = None
    try:
        api = GooglePlayAPI(ANDROID_ID)
        api.login(GOOGLE_LOGIN, GOOGLE_PASSWORD, AUTH_TOKEN)
    except Exception as e:
        pass
    return api


def get_info(api, pkg_name):
    details = None
    try: 
        details = api.details(pkg_name)
    except Exception as e:
        pass
    return details
    
        
def crawler(pkg_name):
    api = login()
    info = get_info(api, pkg_name)
    info = api.toDict(info) 
    info = str(info)
    info = info.replace("true", "True")
    info = info.replace("false", "False")
    info = eval(str(info))
    doc = info["docV2"]
    game_name = doc["title"]
    game_name = ftoj(game_name)
    return game_name


if __name__=="__main__":
    pkg_names = check_pkg_name()
    print pkg_names
    handle_pkg_name(pkg_names)

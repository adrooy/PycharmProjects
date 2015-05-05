#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'limingdong'
__doc__ = """the arguments use to create a connetcion to the database.
    "host": host to connect
    "user": user to connect as
    "passwd": password to user
    "db": database to use
    "port": TCP/IP port to connect to, default port is 3306
    "charset": # If supplied, the connection character set will be changed to this character set
    "use_unicode": If True, text-like columns are returned as unicode objects using the connection's character set.
    Otherwise, text-like columns are returned as strings.
    "cursorclass": cursorclass
"""

import MySQLdb
import MySQLdb.cursors


# consts
# IS_TEST = False
# HOST = "127.0.0.1"
# USER = "test"
# PWD = "test"
# DB = "test"
# PORT = 3306
IS_TEST = False

HOST = "localhost"
USER = "forum"
PWD = "VQq*d@GY4F7J6]MP"
DB = "forum"
PORT = 3306

if IS_TEST:
    HOST = "192.168.1.45"
    USER = "root"
    PWD = "111111"
    DB = "forum"
    PORT = 3306

 #   HOST = "localhost"
  #  USER = "root"
  #  PWD = "215481379"
 #   DB = "forum"
  #  PORT = 3306


print HOST

OPTIONS = {
    "52DictCursor": {
        "host": "116.255.129.52",
        "user": "root",
        "passwd": "ngDm-J)KNPn77SLW",
        "db": "forum",
        "port": 3306,
        "charset": "utf8",
        "use_unicode": False,
        "cursorclass": MySQLdb.cursors.DictCursor,
    },
    "DictCursor": {
        "host": HOST,
        "user": USER,
        "passwd": PWD,
        "db": DB,
        "port": PORT,
        "charset": "utf8",
        "use_unicode": False,
        "cursorclass": MySQLdb.cursors.DictCursor,
    },
    "Cursor": {
        "host": HOST,
        "user": USER,
        "passwd": PWD,
        "db": DB,
        "port": PORT,
        "charset": "utf8",
        "use_unicode": False,
        "cursorclass": MySQLdb.cursors.Cursor,
    },
    # test
    "localhost": {
        "host": "localhost",
        "user": "test",
        "passwd": "test",
        "db": DB,
        "port": 3306,
        "charset": "utf8",
        "use_unicode": False,
        "cursorclass": MySQLdb.cursors.Cursor,
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

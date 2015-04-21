#!/usr/bin/python
#-*- coding:utf-8 -*-


import MySQLdb
import MySQLdb.cursors


IS_TEST = False

if IS_TEST:
    OPTIONS = {
        "GGCursor": {
            "host": "192.168.1.45",
            "user": "root",
            "passwd": "111111",
            "db": "forum",
            "port": 3306,
            "charset": "utf8",
            "use_unicode": False,
#           "cursorclass": MySQLdb.cursors.GGCursor,
        },
        "AppMarketCursor": {
            "host": "116.255.240.168",
            "user": "appmarket",
            "passwd": "HyZkygUEe08qcfan",
            "db": "appmarket",
            "port": 3306,
            "charset": "utf8",
            "use_unicode": False,
#           "cursorclass": MySQLdb.cursors.AppMarketCursor,
        },
        "UCApkInfoCursor": {
            "host": "116.255.240.168",
            "user": "appmarket",
            "passwd": "HyZkygUEe08qcfan",
            "db": "appmarket",
            "port": 3306,
            "charset": "utf8",
            "use_unicode": False,
#           "cursorclass": MySQLdb.cursors.UCApkInfoCursor,
        }
    }
else:
    OPTIONS = {
        "GGCursor": {
            "host": "106.187.54.178",
            "user": "root",
            "passwd": "ngDm-J)KNPn77SLW",
            "db": "forum",
            "port": 3306,
            "charset": "utf8",
            "use_unicode": False,
#           "cursorclass": MySQLdb.cursors.GGCursor,
        },
        "45Cursor": {
            "host": "192.168.1.45",
            "user": "root",
            "passwd": "111111",
            "db": "forum",
            "port": 3306,
            "charset": "utf8",
            "use_unicode": False,
#           "cursorclass": MySQLdb.cursors.AppMarketCursor,
        },
        "UCApkInfoCursor": {
            "host": "116.255.240.168",
            "user": "appmarket",
            "passwd": "HyZkygUEe08qcfan",
            "db": "appmarket",
            "port": 3306,
            "charset": "utf8",
            "use_unicode": False,
#           "cursorclass": MySQLdb.cursors.UCApkInfoCursor,
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
#cursorclass = settings.get("cursorclass")
#    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset, use_unicode=use_unicode, cursorclass=cursorclass)
    conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port, charset=charset, use_unicode=use_unicode)
    return conn

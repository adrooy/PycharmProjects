#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: browser.py
Author: limingdong
Date: 6/20/14
Description: 伪装浏览器
"""

import urllib2
import cookielib
import random
import utils
from ua import choose
from logs import logger


def read_proxy(url, referer):
    proxy = random.choice(utils.read_proxy_file())
    print proxy
    protocol, pro = proxy.split('=')
    proxy_support = urllib2.ProxyHandler({protocol.lower(): '%s//%s' % (protocol.lower(), pro)})
    http_handler = urllib2.HTTPHandler(debuglevel=1)
    https_handler = urllib2.HTTPSHandler(debuglevel=1)
    handlers = [proxy_support, http_handler, https_handler]
    # handlers = [proxy_support]

    headers = {
        'User-Agent': choose(),
        'Referer': referer,
        'Content-Type': 'text/html',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-encoding': 'gzip'
    }
    req = urllib2.Request(
        url=url,
        headers=headers
    )
    content = ""
    try:
        opener = urllib2.build_opener(*handlers)
        response = opener.open(req, timeout=10)
        content = response.read()
        response.close()
    except Exception, e:
        logger.debug("search(%s): %s .error.", url, str(e))
    return content


def read(url, referer):

    content = ""
    ua = choose()
    headers = {
        'User-Agent': ua,
        'Referer': referer,
        'Content-Type': 'text/html',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip'  # 以gzip下载html，降低网络资源负荷
    }

    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))

    req_referer = urllib2.Request(
        url=referer,
        headers=headers
    )

    opener.open(req_referer, timeout=10)  # 用于记录cookie

    req = urllib2.Request(
        url=url,
        headers=headers
    )
    try:
        result = opener.open(req, timeout=20)

        import StringIO
        import gzip
        predata = result.read()
        stream = StringIO.StringIO(predata)
        gzipper = gzip.GzipFile(fileobj=stream)
        try:
            content = gzipper.read()
            print "OK"
        except:
            #如果服务器不支持gzip，那么就直接下载网页
            content = predata
        result.close()
    except urllib2.HTTPError, e:
        logger.error("Error Code: %s. Reason: %s. Request URL: %s", str(e.code), str(e.reason), url)
    except urllib2.URLError, e:
        logger.error("Error Reason: %s. Request URL: %s", str(e.reason), url)
    return content


class RedirectHandler(urllib2.HTTPRedirectHandler):

    def __init__(self):
        pass

    def http_error_302(self, req, fp, code, msg, headers):
        return headers['Content-Length']


def get_data_size(url, referer):
    ua = choose()
    headers = {
        'User-Agent': ua,
        'Referer': referer,
        'Content-Type': 'text/html',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch'
    }

    req = urllib2.Request(
        url=referer,
        headers=headers
    )

    try:
        opener = urllib2.build_opener(RedirectHandler)
        response = opener.open(req, timeout=10)
        # print "search..."
        # print "%s ===> %s" % (url, response)
        # print dir(response)
        # print response.headers
    except Exception, e:
        response = None
        logger.debug("search(%s): %s .error.", url, str(e))
    if response:
        content = response.headers['Content-Length']
    else:
        content = 0
    return content


def test():
    # url = "http://app.mi.com/detail/49150"
    # referer = "http://app.mi.com"
    # # content = read_proxy(url, referer)
    # content = read(url, referer)
    # print content
    # print content == ""
    url = 'http://gdown.baidu.com/data/wisegame/f68709112d327a44/LittleCommander_56.apk'
    print get_data_size(url, url)

if __name__ == '__main__':
    test()
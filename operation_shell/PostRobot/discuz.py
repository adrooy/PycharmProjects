#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" description
dz 发帖: 两种方式 修改数据库和模拟登录
"""
# FIXME: 删除修改数据库发帖方式的代码

__author__ = 'wangfei'
__date__ = '2015/03/25'

import time
import logging

logger = logging.getLogger(__name__)


def post(conn, subject, message, fid=52, author='robot', authorid=68):
    """通过修改数据库来自动发帖
    :param conn: MySQLdb Connection instance
    :param subject: 帖子主题
    :param message: 帖子内容
    :param fid: 帖子板块
    :param author: 发帖人
    :param authorid: 发帖人id
    :return tid(帖子id)
    """
    now = int(time.time())

    # 插入 pre_forum_post_tableid 表,获取pid
    cursor_pid = conn.cursor()
    sql_pid = 'insert into pre_forum_post_tableid values(null)'
    cursor_pid.execute(sql_pid)
    pid = cursor_pid.lastrowid

    # 插入 pre_forum_thread 表,获取tid
    cursor_tid = conn.cursor()
    sql_tid = '''insert into pre_forum_thread
                (fid, posttableid, typeid, sortid, readperm, price, author, authorid, subject, dateline, lastpost,
                lastposter, views, replies, displayorder, highlight, digest, rate, special, attachment, moderated,
                closed, stickreply, recommends, recommend_add, recommend_sub, heats, status, isgroup, favtimes,
                sharetimes, stamp, icon, pushedaid, cover, replycredit, relatebytag, maxposition, bgcolor, comments,
                hidden) values
                (%s, 0, 0, 0, 0, 0, "%s", %s, "%s", %s, %s, "%s", 1, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 32, 0, 0, 0, -1, -1,
                0, 0, 0, 0, 0, "", 0, 0)''' % (fid, author, authorid, subject, now, now, author)
    cursor_tid.execute(sql_tid)
    tid = cursor_tid.lastrowid

    # 插入 pre_forum_post 表
    cursor_post = conn.cursor()
    sql_post = '''insert into pre_forum_post
                (pid, fid, tid, first, author, authorid, subject, dateline, message, useip, port, invisible, anonymous,
                usesig, htmlon, bbcodeoff, smileyoff, parseurloff, attachment, rate, ratetimes, status, tags, comment,
                replycredit) values
                (%s, %s, %s, 1, "%s", %s, "%s", %s, "%s", "localhost", 8888, 0, 0, 1, 0, -1, -1,
                0, 0, 0, 0, 0, "", 0, 0)''' % (pid, fid, tid, author, authorid, subject, now, message)
    cursor_post.execute(sql_post)

    # 更新 pre_forum_forum 表,更新板块帖子数等
    lastpost = '\t'.join([str(tid), subject, author])
    cursor_forum = conn.cursor()
    sql_forum = '''update pre_forum_forum set threads=threads+1, posts=posts+1, lastpost="%s"
                where fid=%s''' % (lastpost, fid)
    cursor_forum.execute(sql_forum)

    # 更新 pre_common_member_count 表,更新用户发帖数
    cursor_count = conn.cursor()
    sql_count = '''update pre_common_member_count set extcredits2=extcredits2+2, posts=posts+1, threads=threads+1
                where uid=%s''' % authorid
    cursor_count.execute(sql_count)

    return tid


import cookielib
import urllib2
import urllib
import re


class Discuz(object):
    """模拟登录自动发帖
    """

    def __init__(self, user, password, login_url, login_submit_url, post_url, post_submit_url, referer):
        self.username = user
        self.password = password
        self.login_url = login_url
        self.login_submit_url = login_submit_url
        self.post_url = post_url
        self.post_submit_url = post_submit_url
        self.referer = referer

        self.regex = {
            'login_reg': '<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            'post_reg': '<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            'tid_reg': '<link\s*href="([\w\W]+?)"\s*rel="canonical"\s*\/>'
        }
        self.logined = False
        self.login()

    def login(self):
        try:
            # 初始化cookie
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Mozilla/4.0 ' \
                         '(compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 2.0.507'
            opener.addheaders = [('User-agent', user_agent)]
            urllib2.install_opener(opener)

            # 抓取登录页(login_url)获取formhash
            login_page = urllib2.urlopen(self.login_url).read()
            formhash = re.search(self.regex['login_reg'], login_page).group(1)

            # post数据到(login_submit_url)
            login_data = urllib.urlencode({
                'posttime': str(int(time.time())),
                'formhash': formhash,
                'loginfield': 'username',
                'username': self.username,
                'password': self.password,
                'questionid': 0,
                'referer': self.referer})
            login_submit_page = urllib2.urlopen(self.login_submit_url, login_data).read()
            n_pos = login_submit_page.index('succeedmessage')
            if n_pos <= 0:
                raise Exception('login failed')
            self.logined = True
        except Exception as e:
            logger.error('login failed: %s', str(e), exc_info=1)
            self.logined = False

    def _post(self, subject, content):
        # 抓取post页(post_url)获取formhash
        post_page = urllib2.urlopen(self.post_url).read()
        formhash = re.search(self.regex['post_reg'], post_page).group(1)
        # post数据到(post_submit_url)
        post_data = urllib.urlencode({
            'allownoticeauthor': '1',
            'posttime': str(int(time.time())),
            'formhash': formhash,
            'message': content,
            'subject': subject,
            'usesig': '1',
            'wysiwyg': '1'})
        post_submit_page = urllib2.urlopen(self.post_submit_url, post_data).read()
        tid_url = re.search(self.regex['tid_reg'], post_submit_page)
        if tid_url is None:
            raise Exception('post error')
        else:
            tid_url = tid_url.group(1)
            tid = int(tid_url[tid_url.find('tid=') + 4:])
        return tid

    def post(self, subject, content, retry=3):
        """
        :param subject: 帖子主题
        :param content: 帖子内容
        :param retry: 重试次数
        :return: tid(帖子id)
        """
        ret = None
        for _ in xrange(retry + 1):
            try:
                ret = self._post(subject, content)
            except Exception as e:
                logger.warn('post wrong, retry: %s', e)
                time.sleep(2)
                continue

        if ret is None:
            raise Exception('retry %s count, but failed still. subject: %s' % subject)

        return ret


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)-15s %(levelname)s:%(module)s] %(message)s')
    import MySQLdb

    con = MySQLdb.Connection(host='192.168.1.45', user='root', passwd='111111', db='forum', charset='utf8')

    t0 = time.time()
    print post(con, '测试1', '测试消息1')
    print time.time() - t0

    # ---------两种发帖方式分割线-----------

    HOST = 'http://192.168.1.45'
    FID = 52
    options = dict(user='robot', password='lbesecdch',
                   login_url=HOST + '/forum/member.php?mod=logging&action=login',
                   login_submit_url=HOST + '/forum/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=L'
                                           'UPyq&inajax=1',
                   post_url=HOST + '/forum/forum.php?mod=post&action=newthread&fid=%s' % FID,
                   post_submit_url=HOST + '/forum/forum.php?mod=post&action=newthread&'
                                          'fid=%s&extra=&topicsubmit=yes' % FID,
                   referer=HOST + '/forum/index')

    t00 = time.time()
    dz = Discuz(**options)
    print dz.post('测试2', '测试消息2')
    print time.time() - t00
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'duchunhai'
import sys
sys.path.append("/home/mgmt/operation")

from database.mysql_client import connections
from database.mysql_client import IS_TEST
import urllib2, urllib, cookielib
import re
import time
import MySQLdb
import cgi

class Discuz:
    def __init__(self,user,pwd,args):
        self.username = user
        self.password = pwd
        self.args = args
        self.regex = {
            'loginreg': '<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            'replyreg': '<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            'tidreg': '<tbody\s*id="normalthread_\d+">[\s\S]+?<span\s*id="thread_(\d+)">',
            'postreg': '<input\s*type="hidden"\s*name="formhash"\s*value="([\w\W]+?)"\s*\/>',
            'tidreg': '<link\s*href="([\w\W]+?)"\s*rel="canonical"\s*\/>'
        }
        self.conn = None
        self.cur = None
        self.islogin = False
        self.login()

    def login(self):
        try:

            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            user_agent = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; Mozilla/4.0 \
                    (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 2.0.507'
            opener.addheaders = [('User-agent', user_agent)]
            urllib2.install_opener(opener)


            loginurl = self.args['loginurl']

            loginPage = urllib2.urlopen(self.args['loginurl']).read()
            formhash = re.search(self.regex['loginreg'], loginPage)
            formhash = formhash.group(1)

            print 'start login...'


            postime = str(int(time.time()))
            logindata = urllib.urlencode({
                'posttime': postime,
                'formhash': formhash,
                'loginfield': 'username',
                'username': self.username,
                'password': self.password,
                'questionid': 0,
                'referer': self.args['referer']})
            request = urllib2.Request(self.args['loginsubmiturl'], logindata)
            response = urllib2.urlopen(request)
            loginresphtml = response.read()

            nPos = loginresphtml.index('succeedmessage')
            if nPos > 0:
                print('login success...')

        except Exception,e:
                print 'loggin error: %s' % e

    def post(self, fid, subject, content):
        try:
            posturl = self.args['posturl'] % fid
            #print posturl
            loginPage = urllib2.urlopen(self.args['posturl']).read()
            formhash = re.search(self.regex['postreg'], loginPage)
            formhash = formhash.group(1)
            #print 'login formhash:', formhash
            #print 'start post...'
            postime = str(int(time.time()))
            postdata = urllib.urlencode({
                'allownoticeauthor': '1',
                'posttime': postime,
                'formhash': formhash,
                'message': content,
                'subject': subject,
                'usesig': '1',
                'wysiwyg': '1'})
            request = urllib2.Request(self.args['postsubmiturl'] % fid, postdata)
            response = urllib2.urlopen(request)
            rsphtml = response.read()
            #print rsphtml
            self.islogin = True
            tidurl = re.search(self.regex['tidreg'], rsphtml)
            tidstr = '0'
            if tidurl is None:
                print "Post Failed: %s " % subject
                print rsphtml
            else:
                tidurl = tidurl.group(1)
                tidstr = tidurl[tidurl.find('tid=') + 4:]

            #print 'post success...'

            return tidstr
        except Exception, e:
            print 'post error: %s' % e


if __name__ == '__main__':
    username = 'robot'
    password = 'lbesecdch'
    authorid = 68
    host = 'http://www.ggzs.me'

    if IS_TEST:
        host = 'http://192.168.1.45'

    args = {
        'loginurl': host + '/forum/member.php?mod=logging&action=login',
        'loginsubmiturl': host + '/forum/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LUPyq&inajax=1',
        'posturl': host + '/forum/forum.php?mod=post&action=newthread&fid=%s',
        'postsubmiturl': host + '/forum/forum.php?mod=post&action=newthread&fid=%s&extra=&topicsubmit=yes',
        'referer': host + '/forum/index'
    }
    dz = Discuz(username, password, args)
    fid = '53'
    # tid = dz.post(fid, "第5帖", "第一帖第一帖第一帖第一帖第一帖")

    conn = conn = connections('Cursor')
    cursor = conn.cursor()

    #查询 and apk_id = 'c8129d3d'
    cursor.execute("select * from iplay_game_pkg_info where (source = 1 or source = 3 or source = 4) and tid = 0 and enabled = 1")
    n = 0
    for row in cursor.fetchall():
        apkId = row[0]
        gameId = row[1]
        marketChannel = row[2]
        gameName = row[3]
        pkgName = row[4]
        verCode = row[6]
        verName = row[7]
        gameDesc = row[14]

        if not gameDesc or len(gameDesc) <= 9:
            gameDesc = "暂无具体描述信息"

        # apkId = apkId.encode("utf-8")
        # marketChannel = marketChannel.encode("utf-8")
        # gameName = gameName.encode("utf-8")
        # pkgName = pkgName.encode("utf-8")
        # verName = verName.encode("utf-8")
        # gameDesc = gameDesc.encode("utf-8")
        verCode = str(verCode)

        subject = gameName + "[" + apkId + "]"
        message = gameDesc
        if len(message) > 1000:
            message = message[0:900] + "..."
        #message = gameName + "\n下载渠道 :" + marketChannel +"\n游戏包名 :" + pkgName + "\n版本号：" + verCode + "\n版本名称：" + verName + "\n游戏描述：" + gameDesc

        tid = row[8]

        format_subject = cgi.escape(subject)

        tcnt = cursor.execute("select * from pre_forum_thread where subject = \"%s\" and authorid = %d and fid = %d and displayorder >= 0" % (format_subject, authorid, int(fid)))
        if tcnt > 0:
            row = cursor.fetchall()[0]
            exist_tid = row[0]
            int_exist_tid = int(exist_tid)
            exist_posturl = "forum/forum.php?mod=viewthread&tid=%s" % exist_tid
            cursor.execute("update iplay_game_pkg_info set tid = %d, post_url = '%s' where apk_id = '%s'" % (int_exist_tid, exist_posturl.encode('UTF-8'), apkId))
            # print 'has update pkg:tid  for this game : %s' % gameName
            n += 1
            continue

        #print subject
        #print message

        tid = dz.post(fid, subject, message)
        tid_mid = r'thread-(\d+?)-' 
        tid = re.findall(tid_mid, tid)[0]
        print tid
        inttid = int(tid)
        if inttid != 0:
            posturl = "forum/forum.php?mod=viewthread&ping=1&tid=%s" % tid
            cursor.execute("update iplay_game_pkg_info set tid = %d, post_url = '%s' where apk_id = '%s'" % (inttid, posturl.encode('UTF-8'), apkId))
            print 'create thread and update pkg info for gamename (%s) tid is (%s)' % (subject, tid)
    print "update %d pkg tid" % n

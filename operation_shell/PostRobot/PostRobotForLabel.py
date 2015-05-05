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
            #print postdata
            request = urllib2.Request(self.args['postsubmiturl'] % fid, postdata)
            response = urllib2.urlopen(request)
            rsphtml = response.read()
            #print(rsphtml)
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

    threadurlbase = 'forum/forum.php?mod=viewthread&tid='

    args = {
        'loginurl': host + '/forum/member.php?mod=logging&action=login',
        'loginsubmiturl': host + '/forum/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LUPyq&inajax=1',
        'posturl': host + '/forum/forum.php?mod=post&action=newthread&fid=%s',
        'postsubmiturl': host + '/forum/forum.php?mod=post&action=newthread&fid=%s&extra=&topicsubmit=yes',
        'referer': host + '/forum/index'
    }
    dz = Discuz(username, password, args)
    fid = '52'
    # tid = dz.post(fid, "第5帖", "第一帖第一帖第一帖第一帖第一帖")

    conn = conn = connections('Cursor')
    cursor = conn.cursor()

    #查询  and game_id = '9e48c7dd'
    cursor.execute("select * from iplay_game_label_info where (source = 1 or source = 3 or source = 4) and tid = 0 and enabled = 1")
    n = 0
    for row in cursor.fetchall():
        gameId = row[0]
        gameName = row[1]
        gameDesc = row[10]
        tid = row[8]

        if gameName == '/ ESCAPE \\':
            gameName = 'ESCAPE'
        html = cgi.escape(gameName)
        print tid
        print gameId
        print gameName

        '''
        print "select * from pre_forum_thread where subject = \"%s\" and authorid = %d and fid = %d and displayorder >= 0" % (html, authorid, int(fid))
        tcnt = cursor.execute("select * from pre_forum_thread where subject = \"%s\" and authorid = %d and fid = %d and displayorder >= 0" % (html, authorid, int(fid)))
        if tcnt > 0:
            row = cursor.fetchall()[0]
            exist_tid = row[0]
            int_exist_tid = int(exist_tid)
            exist_posturl = "forum/forum.php?mod=viewthread&tid=%s" % exist_tid
            cursor.execute("update iplay_game_label_info set tid = %d, post_url = '%s' where game_id = '%s'" % (int_exist_tid, exist_posturl, gameId))
            # print 'has update label:tid for this game : %s' % gameName
            n += 1
            continue
        '''

        if not gameDesc or len(gameDesc) <= 9:
            gameDesc = gameName + "暂无具体描述信息"
        if len(gameDesc) > 1000:
            gameDesc = gameDesc[0:900] + "..."

        tid = dz.post(fid, gameName, gameDesc)
        tid_mid = r'thread-(\d+?)-' 
        tid = re.findall(tid_mid, tid)[0]
        print tid
        inttid = int(tid)
        if inttid != 0:
            posturl = "forum/forum.php?mod=viewthread&ping=1&tid=%s" % tid
            cursor.execute("update iplay_game_label_info set tid = %d, post_url = '%s' where game_id = '%s'" % (inttid, posturl, gameId))
            print 'create thread and update label info for game (%s) tid is (%s)' % (gameName, tid)

    print "update %d label tid" % n

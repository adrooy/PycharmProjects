#!/usr/bin/python
#-*- coding:utf-8 -*-


import os
import sys


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
#'cat gamecommunity.log.2015-03-18 | tail -n +1000000 | head -n 2000000 > aaa'
def pre_handle_file(filename):
    num = 1
    readfile = os.path.join(BASE_DIR, filename)
#    readfile = os.path.join(BASE_DIR, filename)
    while True:
        goalfile = os.path.join(BASE_DIR, 'tmp', filename + '.' + str(num))
        start = 1000000*(num-1) + 1
        end = 1000000*num
        cmd = 'cat %s | tail -n +%d | head -n %d > %s' % (readfile, start, end, goalfile)
        os.system(cmd)
        num += 1
        if not len(open(goalfile).read()):
            break


def handle_file(filename):
    causes = {}
    for i in os.walk(os.path.join(BASE_DIR, 'tmp')):
        dirpath = i[0]
        filenames = i[2]
        for name in filenames:
            if filename in name:
                with open(os.path.join(dirpath, name)) as files:
                    for line in files:
                        if 'ERROR' in line:
                            line_info = line.split('ERROR')[1].split(':')
                            cause = line_info[0]
                            if cause not in causes:
                                causes[cause] = 1
                            else:
                                causes[cause] += 1
    results = sorted(causes.items(), key=lambda d: d[1], reverse=True) 
    with open(os.path.join(BASE_DIR, '%s.csv' % filename), 'w') as files:
        for cause in results:
            files.write(str(cause[1]))
            files.write(cause[0])
            files.write('\n')
if len(sys.argv) != 2:
    print '请输入要分析的日志文件名'
else:
    filename = sys.argv[1]
    pre_handle_file(filename)
    handle_file(filename)

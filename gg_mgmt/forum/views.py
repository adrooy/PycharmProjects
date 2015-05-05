#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: views.py
Author: xiangxiaowei
Date: 14/04/15
Description:
"""


import os
import json
import time
import logging
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.models import User

from forum.models import *


log = logging.getLogger('error')


types = [
    {'id': '1', 'name': '游戏安装时'},
    {'id': '2', 'name': '把手'},
    {'id': '3', 'name': '闪屏'},
    {'id': '4', 'name': '通知栏'},
    {'id': '5', 'name': '应用推荐'}
]
target_types = [
    {'id': '0', 'name': '不可点击'},
    {'id': '1', 'name': '网页地址'},
    {'id': '2', 'name': '游戏详情页'},
    {'id': '3', 'name': '应用下载地址'}
]


@csrf_exempt
@login_required
def index(request):
    username = request.user
    user = User.objects.get(username=username)
    editor = IplayEditorInfo.objects.get(name=user.last_name+user.first_name)
    infos = IplayGameLabelInfo.objects.filter(source=3)
    return render_to_response('iplay_ad_info.html', {
        'infos': infos,
        'user': editor,
        'editor': editor,
    }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def iplay_ad_info(request):
    username = request.user
    user = User.objects.get(username=username)
    editor = IplayEditorInfo.objects.get(name=user.last_name+user.first_name)
    channel = request.GET.get('channel')
    type = request.GET.get('type')
    channel = channel if channel else 'A100'
    type = type if type else '0'
    if type != '0':
        infos = IplayAdInfo.objects.filter(channel=channel, type=type).order_by('order_num')
    else:
        infos = IplayAdInfo.objects.filter(channel=channel).order_by('order_num')
    log.debug(infos)
    num = 1
    for info in infos:
        info.order_num = num
        info.type = str(info.type)
        IplayAdInfo.objects.filter(id=info.id, channel=channel).update(order_num=info.order_num)
        num += 1
    channels = IplayToolAdChannelMapping.objects.all()
    return render_to_response('iplay_ad_info.html', {
        'infos': infos,
        'types': types,
        'channels': channels,
        'type': type,
        'channel': channel,
        'user': editor,
        'editor': editor,
    }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def edit_iplay_ad(request):
    username = request.user
    user = User.objects.get(username=username)
    editor = IplayEditorInfo.objects.get(name=user.last_name+user.first_name)
    id = request.GET.get('id')
    channel = request.GET.get('channel')
    type = request.GET.get('type')
    if id and channel:
        info = IplayAdInfo.objects.get(id=id, channel=channel) if id else {}
        chs = IplayAdInfo.objects.filter(id=id)
        if info.filter_pkg_names:
            info.filter_pkg_names = json.loads(info.filter_pkg_names)
        info.type = str(info.type)
        info.target_type = str(info.target_type)
    else:
        info = {
            'channel': channel,
            'type': type
        }
        chs = {}
    channels = IplayToolAdChannelMapping.objects.all()
    return render_to_response('edit_iplay_ad.html', {
        'info': info,
        'chs': chs,
        'types': types,
        'target_types': target_types,
        'channels': channels,
        'user': editor,
        'editor': editor,
    }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def add_iplay_ad(request):
    response=HttpResponse()
    response['Content-Type'] = 'text/string'
    id = request.POST.get('id', '')
    type = request.POST.get('type')
    package_name = request.POST.get('package_name')
    order_num = request.POST.get('order_num')
    title = request.POST.get('title')
    content = request.POST.get('content')
    pic_url = request.POST.get('pic_url')
    big_pic_url = request.POST.get('big_pic_url')
    target_type = request.POST.get('target_type')
    target = request.POST.get('target')
    pkg_name = request.POST.get('pkg_name')
    ver_name = request.POST.get('ver_name')
    size = request.POST.get('size')
    filename = request.POST.get('filename')
    show_delay = request.POST.get('show_delay')
    next_delay = request.POST.get('next_delay')
    chs = request.POST.get('chs').split(',')
    filter_pkg_names = json.dumps(request.POST.get('filter_pkg_names').split(','))
    channel = request.POST.get('channel')
    life_time = request.POST.get('life_time')
    monet_silent = request.POST.get('monet_silent')
    wifi_silent = request.POST.get('wifi_silent')
    download_dismissible = request.POST.get('download_dismissible')
    install_dismissible = request.POST.get('install_dismissible')
    size = size if size else 0
    show_delay = show_delay if show_delay else 120
    next_delay = next_delay if next_delay else 43200
    life_time = life_time if life_time else 48
    wifi_silent = wifi_silent if wifi_silent else 0
    monet_silent = monet_silent if monet_silent else 0
    download_dismissible = download_dismissible if download_dismissible else 0
    install_dismissible = install_dismissible if install_dismissible else 0
    """
    #更新广告内容
    if channel in json.loads(chs):
        log.debug(chs[0])
        log.debug(chs)
        log.debug(id)
        log.debug(channel)
        log.debug('111')
        IplayAdInfo.objects.filter(id=id, channel=channel).update(type=type, package_name=package_name, title=title, content=content,
            pic_url=pic_url, big_pic_url=big_pic_url, target_type=target_type, target=target, pkg_name=pkg_name
            , ver_name=ver_name, size=size, filename=filename, show_delay=show_delay, next_delay=next_delay,
            filter_pkg_names=filter_pkg_names, life_time=life_time, monet_silent=monet_silent,
            wifi_silent=wifi_silent, download_dismissible=download_dismissible, install_dismissible=install_dismissible)
    #新增广告内容
    """
    #新增渠道或者修改广告信息
    if id:
        ads = IplayAdInfo.objects.filter(id=id)
        channels = []
        for ad in ads:
            channels.append(ad.channel)
            #删除渠道下广告
            if ad.channel not in chs:
                channel = ad.channel
                IplayAdInfo.objects.get(id=id, channel=channel).delete()
        for channel in chs:
            if channel not in channels:
                IplayAdInfo(id=id, type=type, package_name=package_name, title=title, content=content, pic_url=pic_url,
                    big_pic_url=big_pic_url, target_type=target_type, target=target, pkg_name=pkg_name
                    , ver_name=ver_name, size=size, filename=filename, show_delay=show_delay, next_delay=next_delay,
                    filter_pkg_names=filter_pkg_names, channel=channel, order_num=0, life_time=life_time, monet_silent=monet_silent
                    , wifi_silent=wifi_silent, download_dismissible=download_dismissible, install_dismissible=install_dismissible).save()
            else:
                IplayAdInfo.objects.filter(id=id, channel=channel).update(type=type, package_name=package_name, title=title, content=content,
                    pic_url=pic_url, big_pic_url=big_pic_url, target_type=target_type, target=target, pkg_name=pkg_name
                    , ver_name=ver_name, size=size, filename=filename, show_delay=show_delay, next_delay=next_delay,
                    filter_pkg_names=filter_pkg_names, life_time=life_time, monet_silent=monet_silent,
                    wifi_silent=wifi_silent, download_dismissible=download_dismissible, install_dismissible=install_dismissible)
    #新增广告，广告id为自增id+1(_id+1)
    else:
        _id = IplayAdInfo.objects.all().order_by('-_id')[0]._id
        for channel in chs:
            IplayAdInfo(id=_id+1, type=type, package_name=package_name, title=title, content=content, pic_url=pic_url,
                big_pic_url=big_pic_url, target_type=target_type, target=target, pkg_name=pkg_name
                , ver_name=ver_name, size=size, filename=filename, show_delay=show_delay, next_delay=next_delay,
                filter_pkg_names=filter_pkg_names, channel=channel, order_num=0, life_time=life_time, monet_silent=monet_silent
                , wifi_silent=wifi_silent, download_dismissible=download_dismissible, install_dismissible=install_dismissible).save()
    log.debug(channel)
    response.write(channel)
    return response


@csrf_exempt
@login_required
def del_iplay_ad(request):
    response=HttpResponse()
    response['Content-Type'] = 'text/string'
    id = request.POST.get('id')
    channel = request.POST.get('channel')
    IplayAdInfo.objects.get(id=id, channel=channel).delete()
    response.write('yes')
    return response


@csrf_exempt
@login_required
def up_iplay_ad(request):
    username = request.user
    user = User.objects.get(username=username)
    editor = IplayEditorInfo.objects.get(name=user.last_name+user.first_name)
    channel = request.GET.get('channel')
    type = request.GET.get('type')
    channel = channel if channel else 'A100'
    type = type if type else '5'
    infos = IplayAdInfo.objects.filter(channel=channel, type=type).order_by('order_num')
    id = int(request.GET.get('id'))
    order_num = IplayAdInfo.objects.get(id=id, channel=channel).order_num
    up_id = IplayAdInfo.objects.get(channel=channel, type=type, order_num=order_num-1).id
    up_num = order_num-1
    IplayAdInfo.objects.filter(id=id, channel=channel).update(order_num=up_num)
    IplayAdInfo.objects.filter(id=up_id, channel=channel).update(order_num=up_num+1)
    log.debug('id: %s, order_num: %s' % (str(id), str(up_num)))
    log.debug('id: %s, order_num: %s' % (str(up_id), str(up_num+1)))
    infos = IplayAdInfo.objects.filter(channel=channel, type=type).order_by('order_num')
    for info in infos:
        info.type = str(info.type)
    channels = IplayToolAdChannelMapping.objects.all()
    return render_to_response('iplay_ad_info.html', {
        'infos': infos,
        'types': types,
        'channels': channels,
        'type': type,
        'channel': channel,
        'user': editor,
        'editor': editor,
    }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def down_iplay_ad(request):
    username = request.user
    user = User.objects.get(username=username)
    editor = IplayEditorInfo.objects.get(name=user.last_name+user.first_name)
    channel = request.GET.get('channel')
    type = request.GET.get('type')
    channel = channel if channel else 'A100'
    type = type if type else '5'
    infos = IplayAdInfo.objects.filter(channel=channel, type=type).order_by('order_num')
    id = int(request.GET.get('id'))
    order_num = IplayAdInfo.objects.get(id=id, channel=channel).order_num
    down_id = IplayAdInfo.objects.get(channel=channel, type=type, order_num=order_num+1).id
    down_num = order_num+1
    IplayAdInfo.objects.filter(id=id, channel=channel).update(order_num=down_num)
    IplayAdInfo.objects.filter(id=down_id, channel=channel).update(order_num=order_num)
    log.debug('id: %s, order_num: %s' % (str(id), str(down_num)))
    log.debug('id: %s, order_num: %s' % (str(down_id), str(order_num)))
    infos = IplayAdInfo.objects.filter(channel=channel, type=type).order_by('order_num')
    for info in infos:
        info.type = str(info.type)
    channels = IplayToolAdChannelMapping.objects.all()
    return render_to_response('iplay_ad_info.html', {
        'infos': infos,
        'types': types,
        'channels': channels,
        'type': type,
        'channel': channel,
        'user': editor,
        'editor': editor,
    }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def plugin_info(request):
    username = request.user
    user = User.objects.get(username=username)
    editor = IplayEditorInfo.objects.get(name=user.last_name+user.first_name)
    infos = IplayUploadPlugin.objects.all().order_by('-id')
    return render_to_response('plugin_info.html', {
        'infos': infos,
        'editor': editor,
    }, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def upload_plugin(request):
    username = request.user
    user = User.objects.get(username=username)
    response=HttpResponse()
    response['Content-Type'] = 'text/string'
    target_pkg_name = request.POST.get('target_pkg_name')
    target_ver_code = request.POST.get('target_ver_code')
    ids = IplayUploadPlugin.objects.filter(is_finished=0, target_pkg_name=target_pkg_name, target_ver_code=target_ver_code)
    if ids:
        msg = 'error'
    else:
        IplayUploadPlugin(target_pkg_name=target_pkg_name, target_ver_code=target_ver_code, is_finished=0,
            editor=user.last_name+user.first_name, save_timestamp=int(time.time())).save()
        plugin = UploadGame.objects.filter(target_pkg_name=target_pkg_name, target_ver_code=target_ver_code).order_by('-id')[0]
        os.system('python /home/xiangxiaowei/Documents/new_post/PostRobot/PostRobotForPlugin.py %s &' % plugin.id)
        msg = 'success'
    response.write(msg)
    return response


@csrf_exempt
@login_required
def search_game(request):
    keyword = request.POST.get('keyword').strip()
    if keyword:
        games = {}
        pkgs = IplayGamePkgInfo.objects.filter(pkg_name=keyword, source=3)
        for index, game in enumerate(pkgs):
            games[str(index)] = [game.game_name, game.pkg_name, game.ver_code]
        return HttpResponse(json.dumps(games))
    else:
        error = ''
        return HttpResponse(error)


@csrf_exempt
@login_required
def release_info(request):
    username = request.user
    user = User.objects.get(username=username)
    editor = IplayEditorInfo.objects.get(name=user.last_name+user.first_name)
    infos = IplayReleaseList.objects.all().order_by('-id')
    return render_to_response('release_info.html', {
        'infos': infos,
        'editor': editor,
    }, context_instance=RequestContext(request))
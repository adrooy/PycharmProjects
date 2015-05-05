#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: urls.py
Author: xiangxiaowei
Date: 04/14/15
Description:
"""

from django.db import models


class IplayAdInfo(models.Model):
    _id = models.IntegerField('id', max_length=11, primary_key=True)
    id = models.IntegerField('广告id', max_length=11)
    type = models.IntegerField('使用场景: type=1,用于游戏安装时的等待页面', max_length=11)
    package_name = models.CharField('游戏id, 可以为空, 表明该位置的缺省广告, 否则是对应某游戏的广告', max_length=512)
    order_num = models.IntegerField('在当前type和game_id下的顺序, 最终返回给客户端时会按照此顺序排序, 缺省广告会排在game_id专有广告之后一起返回', max_length=11)
    title = models.CharField('用于通知栏标题、应用推荐的应用名、安装界面标题等', max_length=1000)
    content = models.TextField('用于通知栏小字、应用推荐中的一句话描述、安装界面文字描述等')
    pic_url = models.CharField('用于通知栏图标、应用推荐图标、安装界面banner图等', max_length=1000)
    big_pic_url = models.CharField('目前只用于通知栏大图标', max_length=1000)
    target_type = models.IntegerField('点击后的跳转目标类型: 0-不可点击 1-网页地址,通过浏览器或webview打开 2-进入GG客户端的游戏详情页,3-通过系统downloadManager下载', max_length=11)
    target = models.CharField('点击后的动作内容,对应type. type是0时可以为空', max_length=1000)
    pkg_name = models.CharField('广告目标的包名', max_length=1000)
    ver_name = models.CharField('版本号', max_length=1000)
    size = models.IntegerField('文件大小，单位byte', max_length=11)
    filename = models.CharField('应用文件名', max_length=1000)
    show_delay = models.IntegerField('广告展示延时,单位s', max_length=11)
    next_delay = models.IntegerField('下次广告展示延时,单位s', max_length=11)
    filter_pkg_names = models.CharField('广告目标的过滤包名列表(json串),当用户安装了filter_pkg_names内的包,会在客户端过滤掉', max_length=1000)
    channel = models.CharField('渠道号', max_length=128)
    life_time = models.IntegerField('广告的生命期,单位h', max_length=11)
    monet_silent = models.IntegerField('移动网络时静默下载(0/1) 0-不静默下载, 1-静默下载', max_length=4)
    wifi_silent = models.IntegerField('wifi时静默下载(0/1) 0-不静默下载, 1-静默下载', max_length=4)
    download_dismissible = models.IntegerField('广告下载通知栏是否可被划去(0/1) 0-不可被划去, 1-可被划去', max_length=4)
    install_dismissible = models.IntegerField('广告安装通知栏是否可被划去(0/1) 0-不可被划去, 1-可被划去', max_length=4)

    class Meta:
        db_table = 'iplay_ad_info'
        verbose_name_plural = '广告平台列表'
        unique_together = ('id', 'channel')


class IplayEditorInfo(models.Model):
    name = models.CharField('编辑名称', max_length=10, primary_key=True)
    icon_url = models.CharField('编辑头像', max_length=200)
    user_desc = models.CharField('小编描述，个性签名', max_length=200)
    display_name = models.CharField('客户端展示名', max_length=10)

    class Meta:
        db_table = 'iplay_editor_info'
        verbose_name_plural = '编辑信息表'


class IplayGameLabelInfo(models.Model):
    game_id = models.CharField('', max_length=8, primary_key=True)
    display_name = models.CharField('', max_length=100)
    icon_url = models.CharField('', max_length=1000)
    source = models.IntegerField('', max_length=10)

    class Meta:
        db_table = 'iplay_game_label_info'
        verbose_name_plural = '游戏label信息表'


class IplayGamePkgInfo(models.Model):
    apk_id = models.CharField('apk_id', max_length=8, primary_key=True)
    game_id = models.CharField('game_id', max_length=8)
    market_channel = models.CharField('渠道', max_length=45)
    game_name = models.CharField('游戏名', max_length=45)
    pkg_name = models.CharField('游戏名', max_length=45)
    ver_code = models.IntegerField('游戏版本号', max_length=11)
    icon_url = models.CharField('游戏icon', max_length=1000)
    source = models.IntegerField('', max_length=10)

    class Meta:
        db_table = 'iplay_game_pkg_info'
        verbose_name_plural = '游戏pkg信息表'


class IplayToolAdChannelMapping(models.Model):
    id = models.CharField('广告渠道id', max_length=64, primary_key=True)
    name = models.CharField('广告渠道名', max_length=128)

    class Meta:
        db_table = 'iplay_tool_ad_channel_mapping'
        verbose_name_plural = '广告平台渠道列表'


class IplayReleaseList(models.Model):
    id = models.IntegerField('发布列表ID', max_length=11, primary_key=True)
    start_date = models.IntegerField('发布开始时间', max_length=11)
    end_date = models.IntegerField('发布结束时间', max_length=11)
    is_finished = models.IntegerField('发布状态', max_length=4)
    msg = models.IntegerField('发布结束信息', max_length=11)

    class Meta:
        db_table = 'iplay_release_list'
        verbose_name_plural = '发布列表'


class IplayUploadPlugin(models.Model):
    id = models.IntegerField('插件入库列表ID', max_length=11, primary_key=True)
    plugin_pkg_name = models.CharField('插件包名', max_length=45)
    plugin_ver_code = models.IntegerField('插件版本号', max_length=11)
    target_pkg_name = models.CharField('目标游戏包名', max_length=45)
    target_ver_code = models.IntegerField('目标游戏版本号', max_length=11)
    editor = models.CharField('插件入库人', max_length=45)
    msg = models.IntegerField('插件入库信息', max_length=11)
    is_finished = models.IntegerField('插件入库状态', max_length=11)
    save_timestamp = models.IntegerField('插件入库开始时间', max_length=11)
    update_timestamp = models.IntegerField('插件入库结束时间', max_length=11)

    class Meta:
        db_table = 'iplay_upload_plugin'
        verbose_name_plural = '插件入库列表'

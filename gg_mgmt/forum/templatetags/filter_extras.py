# -*- coding: utf-8 -*-
import time
from django import template
register = template.Library()


__author__ = 'xiangxiaowei'


@register.simple_tag()
def current_time(timestamp, format_string):
    """Return date from timestamp"""
    return time.strftime(format_string, time.localtime(timestamp))


@register.simple_tag()
def trinocular(condition, true_part, false_part):
    """Trinocular operator"""
    value = true_part if condition else false_part
    return value


@register.simple_tag()
def minue_time(minued, subtrahend):
    """"""
    if minued:
        return round(minued - subtrahend, 2)
    else:
        return round(time.time() - subtrahend, 2)


@register.simple_tag()
def get_groups_old(channel, ads):
    """
    获取可用的渠道(与下发过的渠道去重)
    :param channel: {'id': 'B1', 'name': 'GG助手渠道'}
    :param ads:
    :return:
    """
    channel_ids = []
    for ad in ads:
        channel_ids.append(ad.channel)
    if channel.id in channel_ids:
        return ''
    else:
        return '<option value="'+channel.id+'">'+channel.name+'</option>'
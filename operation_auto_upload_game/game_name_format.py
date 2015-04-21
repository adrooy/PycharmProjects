#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: game_name_format.py
Author: limingdong
Date: 8/26/14
Description: 游戏名字处理
"""

# 不是游戏的tag
TAGS_NOT_GAME = [u"游戏中心", u"攻略", u"辅助", u"神器", u"助手", u"视频", u"论坛", u"秘籍", u"修改器", u"葫芦侠", u"教程",
                 u"作弊码", u"破解器", u"插件", u"实战技巧", u"一键修改", u"游戏存档", u"教你如何打领带"]

# 需要清理掉的版本信息
TAGS_TO_CLEAN = [u"-街机经典无限币版", u"-最新飞行版", u"-红颜缠绵版", u"：米粉特供版", u":米粉特供版", u"-完全安装版", u":摩托车版", u"：圣诞节版", u":圣诞节版",
                 u"-超级版", u"-变态版", u"-史诗版", u"-收集版", u"-白金版", u"-中国版", u"-英文版", u"-土豪版", u":里约版", u"-黄金版", u"-酷跑版", u"-雷霆版",
                 u"-红军版", u"-米粉版", u"-手机版", u"-电信版", u"-标准版", u"街机经典无限币版", u"全解锁无广告版", u"之dota1版", u"万圣节特别版", u"无限币典藏版",
                 u"无限币摇杆版", u"国内官方免费版",
                 u"kakao版", u"忍者切割版", u"市场正式版", u"完全安装版", u"米粉特供版", u"红颜缠绵版", u"精简加强版", u"无限生命版", u"最新飞行版", u"汉化破解版",
                 u"破解免费版", u"内购破解版", u"清晰智能版", u"中文豪华版", u"无限金币版", u"无限金钱版", u"中文破解版", u"免数据包版", u"汉化解锁版", u"夏日少女版",
                 u"腾讯社交版", u"内购免费版",
                 u"moto版", u"圣诞节版", u"bmw版", u"情人节版", u"夏威夷版", u"猎户座版", u"无限命版", u"无限币版", u"摩托车版", u"官方正版", u"之无尽版",
                 u"万圣节版", u"无限制版", u"免验证版", u"去广告版", u"手机版", u"米粉版", u"红军版", u"酷跑版", u"黄金版", u"雷霆版", u"hd版", u"三星版",
                 u"专业版", u"中文版", u"完美版", u"低配版", u"修正版", u"免费版", u"全集版", u"典藏版", u"冒险版", u"初中版", u"升级版", u"真人版", u"叫兽版",
                 u"可爱版", u"后宫版", u"四季版", u"国际版", u"塔防版", u"增强版", u"复刻版", u"夜间版", u"季节版", u"守城版", u"官方版", u"对战版", u"山寨版",
                 u"怀旧版", u"悔棋版", u"战略版", u"抢先版", u"拟真版", u"挑战版", u"超宽版", u"新年版", u"无限版", u"星星版", u"朵拉版", u"极速版", u"格斗版",
                 u"激情版", u"狂欢版", u"畅玩版", u"神兽版", u"竞赛版", u"精英版", u"精装版", u"终极版", u"经典版", u"缠绵版", u"萝莉版", u"街机版", u"解锁版",
                 u"97版", u"运动版", u"进化版", u"迷你版", u"遨遊版", u"金钱版", u"闯关版", u"高级版", u"高通版", u"超级版", u"变态版", u"史诗版", u"收集版",
                 u"白金版", u"中国版", u"英文版", u"土豪版", u"里约版", u"破解版", u"清晰版", u"豪华版", u"最强版", u"金币版", u"土豪版", u"汉化版", u"精简版",
                 u"加强版", u"3d版", u"最新版", u"流畅版", u"离线版", u"高清版", u"完整版", u"修改版", u"免费版", u"炫酷版", u"最终版", u"夏季版", u"开心版",
                 u"无尽版", u"纪念版", u"圣诞版", u"通用版", u"学霸版", u"珍藏版", u"长城版", u"纪念版", u"朋友版", u"冬季版", u"太空版", u"单机版", u"正式版",
                 u"便携版", u"旗舰版", u"图片版", u"春天版", u"直装版", u"pk版", u"二战版", u"西游版", u"贺岁版", u"浪漫版", u"内购版", u"空战版", u"柔情版",
                 u"陆地版", u"爱心版", u"学习版", u"无敌版", u"终结版", u"任务版", u"bt版", u"韩国版", u"军旗版", u"原始版", u"特别版", u"疯狂版", u"童年版",
                 u"移动版", u"天天版", u"竞技版", u"霹雳版", u"电信版", u"标准版", u"美版", u"内购", u"正版", u"新版", u"盗版", u"破解", u"精简",
                 u"清新版", u"代理版",
                 u"完美街机", u"免谷歌", u"官方"]

# 罗马数字对应的keys,和values(须按顺序查找替换)
ROMAN_NUM_KEYS = ['viii', 'vii', 'vi', 'iv', 'iii', 'ii']
ROMAN_NUM_VALUES = ['8', '7', '6', '4', '3', '2']


def format_label_game_name(g_name):
    """
    格式化label_info的游戏名，
    去除**版,
    将全角符号替换为半角符号,
    :param g_name:
    """
    if not isinstance(g_name, unicode):
        g_name = unicode(g_name.lower().replace(" ", ""), "utf-8")

    # 如果游戏名出现不是游戏的名字,返回空值
    for tag in TAGS_NOT_GAME:
        if tag in g_name:
            return ""

    g_name = hot_game_deal(g_name)

    # 去掉游戏中的**版
    for tag in TAGS_TO_CLEAN:
        if tag in g_name:
            g_name = g_name.replace(tag, "")

    # 游戏名不以"["开始,取括号前面值
    if not g_name.startswith("[") and "[" in g_name:
        g_name = g_name.split("[")[0]

    # 游戏名不以"("和"（"开始,取括号前面值
    if not g_name.startswith("(") and "(" in g_name:
        g_name = g_name.split("(")[0]
    elif not g_name.startswith(u"（") and u"（" in g_name:
        g_name = g_name.split(u"（")[0]

    # 游戏名以"("和"（"开始,取括号后的值
    if g_name.startswith("(") and ")" in g_name:
        g_name = g_name.split(")")[1]
    elif g_name.startswith(u"（") and u"）" in g_name:
        g_name = g_name.split(u"）")[1]

    if u"之" in g_name and len(g_name) > 3:
        g_ns = g_name.split(u"之")
        g_n_1 = g_ns[0]
        g_n_2 = g_ns[1]
        if len(g_n_1) > 2 and len(g_n_2) > 1:
            g_name = g_n_1

    if "hd" in g_name:
        g_name = g_name.replace("hd", "")
    # if "3d" in g_name:
    #     g_name = g_name.replace("3d", "")
    if "ol" in g_name:
        g_name = g_name.replace("ol", "")
    if "&middot;" in g_name:
        g_name = g_name.replace("&middot;", "")
    if "..." in g_name:
        g_name = g_name.replace("...", "")

    if "." in g_name:
        g_name = g_name.replace(".", ":")
    elif u"·" in g_name:
        g_name = g_name.replace(u"·", ":")

    # 全角符号替换为":", "--"替换为":"
    if u"：" in g_name:
        g_name = g_name.replace(u"：", ":")
    if "--" in g_name:
        g_name = g_name.replace("--", ":")
    elif "-" in g_name:
        g_name = g_name.replace("-", ":")
    elif u"—" in g_name:
        g_name = g_name.replace(u"—", ":")

    g_name = roman_num_format(g_name)
    return g_name


def hot_game_deal(game_name):
    """
    处理游戏匹配不完整的现象,如(狂野飙车8极速凌云, 史诗塔防2:风之魔咒)
    优先处理
    :param game_name:
    :return:
    """
    games = [u"狂野飙车8:极速凌云", u"史诗塔防2:风之魔咒"]
    for game in games:
        gs = game.split(":")
        if gs[0] in game_name and gs[1] in game_name:
            game_name = gs[0]
    return game_name


def roman_num_format(game_name):
    #处理特殊游戏

    games_ii = [u"龙与地下城ii", u"达芬奇之谜ii", u"武士ii"]
    for g in games_ii:
        if g in game_name:
            game_name = game_name.replace("ii", "2")
            return game_name

    # 处理是否以特殊字符结尾,转换为对应的数字
    for key, value in zip(ROMAN_NUM_KEYS, ROMAN_NUM_VALUES):
        if key in game_name:
            game_name = game_name.replace(key, value)
            break

    return game_name


def test():
    print format_label_game_name("守卫者ii中文版")
    print format_label_game_name(u"守卫者ii中文版")
    print format_label_game_name(u"武士ii：复仇中文版")
    print format_label_game_name(u"武士ii：复仇破解免费版")
    print format_label_game_name(u"帝国塔防ii[圣诞版]")
    print format_label_game_name(u"合金弹头ii(完美街机)")
    print format_label_game_name(u"致命空袭ii-电信版")
    print format_label_game_name(u"小小指挥官2之世界争霸")
    print format_label_game_name(u"植物大战僵尸2-标准版")
    print format_label_game_name(u"狂野飙车8-极速凌云")
    print format_label_game_name(u"狂野飙车8极速凌云")
    print format_label_game_name(u"狂野飙车之极速凌云")
    print format_label_game_name(u"狂也之刃")


if __name__ == "__main__":
    test()
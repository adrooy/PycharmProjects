#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: g_types.py
Author: limingdong
Date: 7/30/14
Description: 
"""

wdj_type_one = ["休闲时间", "跑酷竞速", "宝石消除", "网络游戏", "动作射击", "扑克棋牌", "儿童益智", "塔防守卫", "体育格斗", "角色扮演", "经营策略"]

# wdj_type_two = ["切东西", "找茬", "减压", "宠物", "答题", "音乐节奏", "益智", "解谜",
#                 "跑酷", "赛车", "摩托", "赛艇", "飞机",
#                 "方块", "宝石", "连连看", "祖玛", "泡泡龙", "卡通",
#                 "RPG", "动作竞技", "策略", "卡牌", "经营模拟",
#                 "横版", "射击", "3D", "飞行", "坦克", "狙击",
#                 "斗地主", "棋类", "麻将", "桌游", "德州扑克", "纸牌", "战棋",
#                 "拼图", "识字", "智力开发", "数学",
#                 "闯关", "抢滩登陆",
#                 "街机", "篮球", "足球", "网球", "台球", "其他球类",
#                 "回合制", "即时战斗", "养成", "武侠", "魔幻", "动漫", "三国", "修仙",
#                 "经营", "历史", "战争", "DOTA"]

wdj_type_dict = {
    "休闲时间": ["切东西", "找茬", "减压", "宠物", "答题", "音乐节奏", "益智", "解谜"],
    "跑酷竞速": ["跑酷", "赛车", "摩托", "赛艇", "飞机"],
    "宝石消除": ["方块", "宝石", "连连看", "祖玛", "泡泡龙", "卡通"],
    "网络游戏": ["RPG", "动作竞技", "策略", "卡牌", "经营模拟"],
    "动作射击": ["横版", "射击", "3D", "飞行", "坦克", "狙击"],
    "扑克棋牌": ["斗地主", "棋类", "麻将", "桌游", "德州扑克", "纸牌"],
    "儿童益智": ["拼图", "识字", "智力开发", "数学"],
    "塔防守卫": ["闯关", "抢滩登陆"],
    "体育格斗": ["街机", "篮球", "足球", "网球", "台球", "其他球类"],
    "角色扮演": ["回合制", "即时战斗", "养成", "武侠", "魔幻", "动漫", "三国", "修仙"],
    "经营策略": ["经营", "历史", "战争", "DOTA", "战棋"],
    "破解": ["大型破解", "小型破解", "辅助专区"],
}


def game_type(g_types, game_tags, channel):
    g_type = ""
    if channel == "应用宝":
        g_type = yingyongbao(g_types)
    elif channel == "百度":
        g_type = baidu(g_types)
    elif channel == "360":
        g_type = qihoo360(g_types)
    elif channel == "豌豆荚":
        g_type = wdj(g_types, game_tags)
    elif channel == "安卓市场":
        g_type = hiapk(g_types)
    elif channel == "91":
        g_type = apk91(g_types)
    elif channel == "小米":
        g_type = xiaomi(g_types)
    elif channel == "爱吾":
        g_type = az25(g_types)
    elif channel == "拇指玩":
        g_type = muzhiwan(g_types)
    return g_type


def yingyongbao(g_type):
    result = ""

    if not g_type:
        return result

    if "战略" in g_type:
        return "经营策略"
    if "赛车" in g_type:
        return "跑酷竞速"
    if "网游" in g_type:
        return "网络游戏"
    if "冒险" in g_type:
        return "跑酷竞速"

    for type_one in wdj_type_one:
        if g_type in type_one:
            result = type_one
            break
    return result


def baidu(g_type):
    result = ""

    if not g_type:
        return result

    if "休闲益智" in g_type:
        return "休闲时间"
    if "模拟辅助" in g_type:
        return "跑酷竞速"
    if "体育竞技" in g_type:
        return "动作射击"
    if "赛车竞速" in g_type:
        return "跑酷竞速"
    if "棋牌桌游" in g_type:
        return "扑克棋牌"
    if "经营养成" in g_type:
        return "经营策略"

    for type_one in wdj_type_one:
        if g_type in type_one:
            result = type_one
            break

    return result


def qihoo360(g_type):
    result = ""
    types = []

    if not g_type:
        return result
    if "儿童" in g_type or "智力" in g_type:
        types.append("儿童益智")
    if "动作" in g_type or "对战" in g_type:
        types.append("动作射击")
    if "体育" in g_type or "运动" in g_type:
        types.append("体育格斗")
    if "解迷" in g_type or "经营" in g_type:
        types.append("经营策略")
    if "消遣" in g_type:
        types.append("休闲时间")
    if "模拟器" in g_type or "辅助" in g_type:
        types.append("角色扮演")
    if "AVG" in g_type:
        types.append("养成")
    g_types = g_type.split()
    for g_type in g_types:
        if g_type:
            for type_one in wdj_type_one:
                if g_type in type_one:
                    types.append(type_one)
            for k_type, wdj_type_two in wdj_type_dict.iteritems():
                for type_two in wdj_type_two:
                    if (g_type in type_two) or (type_two in g_type):
                        types.append(k_type)
                        types.append(type_two)
    if types:
        ls = list(set(types))
        ls_sort = sorted(ls, key=lambda ch: len(ch), reverse=True)
        result = "\n".join(ls_sort)
    return result


def wdj(g_type, game_tag):
    if "全部游戏" in g_type:
        g_type = g_type.replace("全部游戏", "")
        if len(g_type) == 0:
            g_type = game_tag
    if "横版" in g_type:
        g_type = "动作射击"
    return g_type


def hiapk(g_type):
    result = ""

    if not g_type:
        return result
    if "网游" in g_type:
        return "网络游戏"
    for type_one in wdj_type_one:
        if g_type in type_one:
            result = type_one
            break

    return result


def apk91(g_type):
    result = ""
    types = []

    if not g_type:
        return result
    g_types = g_type.split()
    for g_type in g_types:
        if g_type:
            g_type = g_type.replace("游戏", "")
            if not g_type:
                continue
            for type_one in wdj_type_one:
                if g_type in type_one:
                    types.append(type_one)
            for k_type, wdj_type_two in wdj_type_dict.iteritems():
                for type_two in wdj_type_two:
                    if (g_type in type_two) or (type_two in g_type):
                        types.append(type_two)
                        types.append(k_type)
    if types:
        ls = list(set(types))
        ls_sort = sorted(ls, key=lambda ch: len(ch), reverse=True)
        result = "\n".join(ls_sort)
    return result


def xiaomi(g_type):
    result = ""

    if not g_type:
        return result

    if "动作枪战" in g_type:
        return "动作射击"
    if "格斗快打" in g_type:
        return "体育格斗"
    if "休闲创意" in g_type:
        return "休闲时间"
    if "塔防迷宫" in g_type:
        return "塔防守卫"

    for type_one in wdj_type_one:
        if g_type in type_one:
            result = type_one
            break
    for k_type, wdj_type_two in wdj_type_dict.iteritems():
        for type_two in wdj_type_two:
            if (g_type in type_two) or (type_two in g_type):
                result = k_type
                break

    return result


def az25(g_type):
    result = ""

    if not g_type:
        return result

    if "休闲" in g_type or "解谜" in g_type or "音乐" in g_type:
        return "休闲时间"
    if "动作" in g_type or "射击" in g_type or "空战" in g_type:
        return "动作射击"
    if "体育" in g_type or "竞技" in g_type:
        return "体育格斗"
    if "赛车" in g_type:
        return "跑酷竞速"
    if "棋牌" in g_type:
        return "扑克棋牌"
    if "经营" in g_type or "战略" in g_type or "养成" in g_type or "冒险" in g_type:
        return "经营策略"
    if "卡牌" in g_type:
        return "网络游戏"
    if "塔防" in g_type:
        return "塔防守卫"
    if "角色" in g_type:
        return "角色扮演"
    if "学习" in g_type or "教育" in g_type:
        return "儿童益智"

    for type_one in wdj_type_one:
        if g_type.replace("游戏", "") in type_one:
            result = type_one
            break

    return result


def muzhiwan(g_type):
    result = ""

    if not g_type:
        return result

    if "休闲益智" in g_type:
        return "休闲时间"
    if "射击" in g_type:
        return "动作射击"
    if "赛车竞速" in g_type:
        return "跑酷竞速"
    if "棋牌" in g_type:
        return "扑克棋牌"
    if "经营" in g_type:
        return "经营策略"
    if "塔防" in g_type:
        return "塔防守卫"
    if "体育" in g_type or "竞技" in g_type:
        return "体育格斗"

    for type_one in wdj_type_one:
        if g_type in type_one:
            result = type_one
            break

    return result


def test():
    type_yyb = ["休闲", "棋牌", "战略", "儿童", "射击", "角色", "动作", "格斗", "赛车", "网游", "冒险", "体育"]
    for yyb in type_yyb:
        print yyb, yingyongbao(yyb)

    # type_bd = ["全部游戏", "休闲益智", "角色扮演", "动作射击", "模拟辅助", "体育竞技", "赛车竞速", "棋牌桌游", "经营养成", "其他游戏"]
    # for bd in type_bd:
    #     print bd, baidu(bd)

    # type_bd = ["全部游戏", "休闲益智", "角色扮演", "动作射击", "模拟辅助", "体育竞技", "赛车竞速", "棋牌桌游", "经营养成", "其他游戏"]
    # for bd in type_bd:
    #     print bd, baidu(bd)

    # type_hiapk = ["休闲", "棋牌", "益智", "射击", "体育", "儿童", "网游", "角色", "策略", "经营", "竞速"]
    # for hi in type_hiapk:
    #     print hi, hiapk(hi)

#     type_apk91 = """赛车竞速
# 跑酷游戏
# 坐车吃饭单手玩
# 花5分钟来一局
#
# """
#     print type_apk91
#     print apk91(type_apk91)

#     type_qihoo = """小编精选
# 动作冒险
# 格斗
# 3D
# 绿色无广告
# 精品单机
# 网络游戏
# 宠物
# 养成
# 回合制
# 休闲益智
# 强联网
# 网游
# 手机网游
# 益智
# 休闲
# 停车
# 汽车
# 路上消遣
#
# """
#     print qihoo360(type_qihoo)

    # type_mi = ["战争策略", "动作枪战", "赛车体育", "网游RPG", "棋牌桌游", "格斗快打", "儿童益智", "休闲创意", "飞行空战", "跑酷闯关", "塔防迷宫", "模拟经营"]
    # for mi in type_mi:
    #     print mi, xiaomi(mi)

    # types = ["体育竞技", "休闲益智", "模拟经营", "动作射击", "赛车竞速", "体育竞技", "策略塔防", "角色扮演", "棋牌游戏"]
    # for t in types:
    #     print t, muzhiwan(t)

    # types = ["益智休闲", "射击游戏", "格斗游戏", "竞速赛车", "体育运动", "卡牌游戏", "动作游戏", "即时角色", "音乐游戏", "恋爱养成"
    # , "冒险游戏", "FPS射击", "探秘解谜", "飞行空战", "学习教育", "即时战略"]
    #
    # for t in types:
    #     print t, az25(t)


if __name__ == "__main__":
    test()
    # for k, v in wdj_type_dict.iteritems():
    #     print k
    #     print v
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: pkg_name_and_baidu_url.py
Author: limingdong
Date: 8/17/14
Description: 
"""

BAIDU_DOWN_URL = {
    # "11人足球先锋":"http://pan.baidu.com/s/1ntFQW4L,游戏为Google Play原版，无需Google Play验证，游戏无需内购。",
    # "EAGolf": "http://pan.baidu.com/s/1kTmOLJh,游戏已经破解Google Play市场验证，但内购破解尚不支持。",
    # "GT赛车2：实车体验": "http://pan.baidu.com/s/1ntoM8QH,游戏已经破解Google Play市场验证，但内购破解尚不支持。",
    # "Millie": "http://pan.baidu.com/s/1sj2l7I1,游戏已经破解Google Play市场验证以及内购，进入游戏在主界面商店可以直接购买付费商品",
    # "阿卡僵尸动物园": "http://pan.baidu.com/s/1xW3Ga,游戏已经破解Google Play市场验证以及内购，进入游戏后点击右下角商城页面购买后，退出游戏并重新进入游戏，内购生效。",
    # "傲气雄鹰2014": "http://pan.baidu.com/s/1jGxaj2m,游戏已经破解Google Play市场验证以及内购，进入游戏通过教学关后在设置中进行购买。",
    # "搏击长空：制空霸权": "http://pan.baidu.com/s/1qWJiEoG,游戏已经破解Google Play市场验证以及内购，进入游戏会有广告，点击右上角X就可以跳过，(广告已透明处理，不会耗费流量)点击右上角市场进入市场，可以解锁全部游戏和购买战机。",
    # "电影之林": "http://pan.baidu.com/s/1pJFMOZ5,游戏已经破解Google Play市场验证以及内购，进入游戏点击+号可以直接购买资源。",
    # "歌剧之谜": "http://pan.baidu.com/s/1bnxo0G3,游戏已经破解Google Play市场验证以及内购，进入游戏后直接选择购买完整版即可获得完整版游戏。",
    # "红牛赛车手": "http://pan.baidu.com/s/1jG3fQ9g,免费购买钻石，免谷歌市场验证",
    # "火线特攻": "http://pan.baidu.com/s/1pJ4X4cN,免验证、内购破解",
    # "饥饿的鲨鱼：进化": "http://pan.baidu.com/s/1lfqTC,游戏已经破解Google Play市场验证以及内购，进入游戏可以内购。",
    # "极限摩托3": "http://pan.baidu.com/s/1mgxCeGo,破解内购、破解谷歌验证",
    # "僵尸之林": "http://pan.baidu.com/s/1vU8jk,游戏已经破解Google Play市场验证以及内购，进入游戏可以内购。",
    # "卡特尔：坟墓守卫者": "http://pan.baidu.com/s/1gdej04N,游戏已经破解Google Play市场验证以及内购，进入游戏可以内购。",
    # "密室逃脱2": "http://pan.baidu.com/s/1qW4V1Ju,游戏已经破解Google Play市场验证以及内购，进入游戏可以内购。",
    # "末日狂奔": "http://pan.baidu.com/s/1jGj3a5o,游戏已经破解Google Play市场验证以及内购，进入游戏可以内购。",
    # "热血格斗2": "http://pan.baidu.com/s/1bneXAk3,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "赛车俱乐部：改装风暴": "http://pan.baidu.com/s/1i3zegBV,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "赏金猎人：黑色黎明": "http://pan.baidu.com/s/1pJwPYkj,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "神秘来信": "http://pan.baidu.com/s/1sj8rnyt,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "死亡之旅": "http://pan.baidu.com/s/1o6ynXvs,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "乌鸦森林之谜2鸦林迷雾": "http://pan.baidu.com/s/1mg0tVg0,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "吸血鬼托德和杰西卡的故事": "http://pan.baidu.com/s/1dDw4zh3,游戏已经破解Google Play市场验证以及内购，进入游戏后直接选择购买完整版即可获得完整版游戏。",
    # "现代战争5": "http://pan.baidu.com/s/1mgqk420,游戏已经破解Google Play市场验证以及内购，进入游戏可以内购。",
    # "英雄传说": "http://pan.baidu.com/s/1pJPqrZt,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "渔人的家庭农场": "http://pan.baidu.com/s/1kT1HREZ,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "羽球杀传奇版2014": "http://pan.baidu.com/s/1qW8toRE,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "足球前锋2": "http://pan.baidu.com/s/1mgqQ5ew,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    # "3D平衡球": "http://pan.baidu.com/s/1mgqQ5ew,游戏已经破解内购及Google Play验证，进入游戏中商店直接购买内购道具即可",
    #
    # "3D平衡球": "http://pan.baidu.com/s/1mgC5rq4,《3D平衡球(3D Ball Free)》是Timuz开发的一款好玩的平衡球休闲游戏。3D平衡球(3D Ball Free)的官方介绍移动你的平衡球到达目的地。游戏拥有优秀的高清图形和令人惊叹的3D环境。",
    # "捕食鱼": "http://pan.baidu.com/s/1bnyA5lH,《捕食鱼（Fish Predator）》是一款3D的大鱼吃小鱼游戏，首先游戏画面有很大程度的提高。",
    # "城市岛屿": "http://pan.baidu.com/s/1i3yyoHR,《城市岛屿 City Island》Android版讲述的是在一座美丽的岛屿上建造自己的城市，你的企业家梦想在这里将成为现实，因为你是第一个到达这个城市的人。",
    # "城市岛屿：机场": "http://pan.baidu.com/s/1eQiVscU,《城市岛屿2 City Island 2 - Building Story》是一款模拟游戏。",
    # "疯狂黑手党": "http://pan.baidu.com/s/1hqy0q2o,《疯狂黑手党》是一款3D双摇杆射击游戏，以黑手党为主角，采用了俯视角来进行操作。",
    # "高速公路赛车": "http://pan.baidu.com/s/1sjCvdKD,《公路竞赛 Highway Racer》是一款炫酷的赛车游戏，游戏属于一款3D画面不错的公路竞速类游戏。",
    # "公路赛车": "http://pan.baidu.com/s/1sjrwvHr,《公路赛车Traffic Racer》是一款竞速类游戏，并且是无止境的竞速",
    # "果冻飞溅": "http://pan.baidu.com/s/1bnldrVD,《果冻飞溅（Jelly Splash）》是一款连线消除游戏，老题材了，画面不错，自带中文。",
    # "合金弹头塔防": "http://pan.baidu.com/s/1c0peYi8,《合金弹头塔防（METAL SLUG DEFENSESNK）》官方推出，传统合金弹头的全新玩法，原版人物融合塔防游戏元素。",
    # "黑暗荒野": "http://pan.baidu.com/s/1mgMEE0o,《黑暗荒野》(Blackmoor)是一款非常具有打击感的动作游戏，风格非常类似于FC时代的魔界村。",
    # "黄金之刃": "http://pan.baidu.com/s/1sjEwYSX,《黄金之剑》一款画面十分华丽的动作角色扮演游戏，采用的是韩式 Q 版风格。",
    # "火爆竞速：碰撞与燃烧": "http://pan.baidu.com/s/1mgyYcAk,《火爆竞速：碰撞与燃烧（Burnin' Rubber Crash n' Burn）》是《火爆竞速4》的官方纪念版。",
    # "急速冲击": "http://pan.baidu.com/s/1i3A95ZZ,《急速冲击》是由Artnumeris制作发行飞行射击游戏，英文名C-RUSH。",
    # "将军的荣耀": "http://pan.baidu.com/s/1i3EDsOX,《将军的荣耀》游戏是一款中文和英文都发行的手机策略游戏，将军的荣耀以二战背景为题材。",
    # "僵尸公路": "http://pan.baidu.com/s/1mgoiKfI,《僵尸公路》是一款赛车类休闲游戏，玩家通过倾斜屏幕来控制汽车的左右移动来进行操作。",
    # "僵尸尖啸": "http://pan.baidu.com/s/1hqDtyF6,《僵尸尖啸》是一款由开发商“Mobigame”开发的跑酷类游戏。",
    # "卡通战争2": "http://pan.baidu.com/s/1gdxgy8z,《卡通战争》是iphone及安卓平台上的一款生存游戏，由Blues制作。现有三个版本。",
    # "口袋商业街": "http://pan.baidu.com/s/1sjJMFJv,《口袋商业街》是一款模拟经营类游戏，主要是以琳琅满目的商店，优质贴心的服务，建设风格新潮的商店、餐厅公寓和丰富多彩的商品来吸引更多顾客光顾！",
    # "拉力漂移赛车": "http://pan.baidu.com/s/1dDktnk1,《拉力漂移赛车(Rally Car Drift Racing 3D)》一款全新的拉力赛车竞速游戏",
    # "美国队长2": "http://pan.baidu.com/s/1c0zUtLe,《美国队长2》是款3D动作类策略游戏，你将控制美国队长进行对战",
    # "迷你忍者": "http://pan.baidu.com/s/1jGxGmwu,《迷你忍者》主要是扮演一个忍者小英雄，在游戏中将通过一连串忍者的训练",
    # "迷你血战2：僵尸": "http://pan.baidu.com/s/1bn3ukiz,《迷你血战2：僵尸》继承前作风格，玩家在此将继续操作我们主角John Gore约翰.戈尔，在关卡内与众多敌军奋斗杀出血路。",
    # "摩托车赛2014": "http://pan.baidu.com/s/1gdkVi6Z,《摩托车赛2014(Bike Racing 2014 Pro)》是一款竞速类游戏，在摩托车赛2014获取到了新的挑战。",
    # "农场小镇": "http://pan.baidu.com/s/1c0kvo2W,《农场小镇英文名（Farm Town）》，是一款模拟经营类游戏，玩家在游戏中扮演一位生活在宁静小镇里的商人",
    # "农场英豪传奇": "http://pan.baidu.com/s/1bnpMXXl,《农场英豪传奇(Farm Heroes Saga)》是King.com开发的一款心爱的三消过关游戏。",
    # "炮艇战3D直升机": "http://pan.baidu.com/s/1eQteFyq,《炮艇战：3D直升机》是一款全3D模拟真实的飞行射击游戏",
    # "沙盒": "http://pan.baidu.com/s/1pJLmAJD,《沙盒》是一款独特的像素游戏。游戏提供玩家一个“物理沙盒”，可以任意修改。",
    # "通天塔大灾难": "http://pan.baidu.com/s/1mgmgRnq,《通天塔大灾难(Babel Rising Cataclysm)》是一款动作游戏，玩家只需轻触指尖，就能让渺小的人类不寒而栗！",
    # "瘟疫公司": "http://pan.baidu.com/s/1jGl4Y8Y,《瘟疫公司》（Plague Inc.）是一款以传染病为题材的策略游戏，由位于英国伦敦的独立游戏工作室Ndemic Creations研发。",
    # "小火苗大冒险": "http://pan.baidu.com/s/1dDcRHBF,《小火苗大冒险》是一款小清新风的休闲游戏，深深爱恋公主的小火苗将使劲全力，向公主证明这段纯朴的爱情不应在灰烬中结束！",
    # "小小起重机": "http://pan.baidu.com/s/1pJK6EOb,《小小起重机 The Little Crane That Could》是一款模拟游戏，控制你的起重机，完成各种任务",
    # "英雄战争2：僵尸病毒": "http://pan.baidu.com/s/1eQ5pV6U,《英雄战争2：僵尸病毒》是款僵尸题材的策略塔防游戏",
    # "殖民地与帝国": "http://pan.baidu.com/s/1o6HQUyY,《殖民地与帝国（Colonies vs Empire）》是一款在线模拟经营游戏。",
    # "装甲飞车": "http://pan.baidu.com/s/1mgE7iaO,《装甲飞车 Armored Car HD》是一款竞速游戏。",
    #
    # "com.gameloft.android.ANMP.GloftDKHM-1": "http://pan.baidu.com/s/1nt1Ei85,",
    # "com.gameloft.android.ANMP.GloftFVHM-1": "http://pan.baidu.com/s/1gdkVyNp,",
    # "狂野之血": "http://pan.baidu.com/s/1dD8GjXf,【破解说明】\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具",
    #
    # '超凡蜘蛛侠': 'http://pan.baidu.com/s/1gdy2I91,【破解说明】\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具"',
    # '超凡蜘蛛侠2': 'http://pan.baidu.com/s/1qW0Snq0,【破解说明】\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具"',
    # '孤胆车神：里约热内卢': 'http://pan.baidu.com/s/1nt0swbv,【破解说明】\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具"',
    # '孤胆车神：拉斯维加斯': 'http://pan.baidu.com/s/1eQpHrYq,【破解说明】\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具"',
    # 'UNO纸牌com.gameloft.android.GloftUNOG-1': 'http://pan.baidu.com/s/1bntRiTx,【破解说明】\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具"',
    # '美国队长com.gameloft.android.ANMP.GloftCPHM-1': 'http://pan.baidu.com/s/1zsQDo,【破解说明】\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具"',
    # 'com.gameloft.android.ANMP.GloftD4HM': 'http://pan.baidu.com/s/1kTxEETx, \n20140913更新：已更新至官方最新版，如内购后游戏崩溃，重新进入游戏即可\n【破解说明】如内购崩溃，重新进入后即完成内购\n1、该游戏已经破解内购及Google Play验证\n2、进入游戏，可直接进入商店购买内购道具'
    'FIFA15UT': 'http://pan.baidu.com/s/1pJBJSk7, \n由游戏大厂EA（艺电）打造的手游作品《FIFA15：终极队伍》（FIFA 15 Ultimate Team），已经正式登陆，玩家可以从500个球队、10000多名球员中网罗自己喜欢的，从而打造属于自己的强大球队。'

}


# for k, v in BAIDU_DOWN_URL.iteritems():
#     print k
#     print v
#     print
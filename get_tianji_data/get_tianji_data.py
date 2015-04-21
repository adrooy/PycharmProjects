#!/usr/bin/python
#-*- coding:utf-8 -*-


import sys
from mysql_client import connections
from logs import logger

reload(sys)
sys.setdefaultencoding("utf-8")


ANDROID = {'1': u'Android 1.0以上',
           '2':u'Android 1.1以上',
           '3':u'Android 1.5以上',
           '4':u'Android 1.6以上',
           '5':u'Android 2.0以上',
           '6':u'Android 2.0.1以上',
           '7':u'Android 2.1以上',
           '8':u'Android 2.2以上',
           '9':u'Android 2.3以上',
           '10':u'Android 2.3.3以上',
           '11':u'Android 3.0以上',
           '12':u'Android 3.1以上',
           '13':u'Android 3.2以上',
           '14':u'Android 4.0以上',
           '15':u'Android 4.0.3以上',
           '16':u'Android 4.1以上',
           '17':u'Android 4.2以上',
           '18':u'Android 4.3以上',
           '19':u'Android 4.4以上',
           '20':u'Android 4.4以上',
           '21':u'Android 5.0以上',
           '22':u'Android 5.1以上'
          }

COLOR_LABELS = {'1': u'免内购', '9': u'有内购', '10': u'无内购',  # 20150306
#                '2': u'破解',  # 20150306
                '3': u'插件',
                '4': u'存档',
                '5': u'免谷歌市场', '11': u'需谷歌市场', '12': u'无需谷歌市场',  # 20150306
                '6': u'免ROOT游戏',
                '7': u'玩家上传',
                '8': u'内侧',

                '13': u'全程联网', '14': u'单机游戏',  # 20150306
                '15': u'破解VPN', '16': u'需VPN', '17': u'无需VPN',  # 20150306
                '18': u'已汉化'}  # 20150306




def get_star(cnt):
    return 6 + cnt/300000


def get_label_info(game_id):
    conn = connections("GGCursor")
    cursor = conn.cursor()
    sql = """
    SELECT game_id, display_name, icon_url, color_label, star_num, game_language, developer, detail_desc, short_desc, gg_download_cnt,origin_types, screen_shot_urls, from_unixtime(save_timestamp),detail_desc_html  FROM iplay_game_label_info WHERE game_id='%s'
    """ % game_id
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_gg_need_check_data error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    for row in rows:
        result = {}
        game_id = row[0]
        display_name = row[1].replace(': ', ':').split(' ')[0]
        icon_url = row[2]
        color_label = row[3]
        colors = []
        for color in color_label.split('\n'):
            if color in COLOR_LABELS:
                colors.append(COLOR_LABELS[color])
        color_label = ','.join(colors)
        language = row[5] if row[5] else ''
        developer = row[6] if row[6] else ''
        detail_desc = row[7] 
        short_desc = row[8] 
        gg_download_cnt = row[9] if row[9] else 0
        origin_types = row[10]
        types = []
        for origin in origin_types.split('\n'):
            if origin:
                types.append(origin)
        origin_types = ','.join(types)
        screen_shot_urls = row[11].replace('\n', ',')
        save_time = str(row[12]).split(' ')[0]
        detail_desc_html = row[13]
        star_num = get_star(gg_download_cnt)
        if detail_desc_html:
            detail_desc = detail_desc_html
        '''
        print 'game_id: %s' % game_id
        print '\n'
        print 'display_name: %s' % display_name
        print '\n'
        print 'icon_url: %s' % icon_url
        print '\n'
        print 'color_label: %s' % color_label
        print '\n'
        print 'language: %s' % language
        print '\n'
        print 'developer: %s' % developer
        print '\n'
        print 'star_num: %s' % str(star_num)
        print '\n'
        #print 'detail_desc: %s' % detail_desc
        print '\n'
        #print 'short_desc: %s'  % short_desc
        print '\n'
        print 'gg_download_cnt: %s' % gg_download_cnt
        print '\n'
        print 'origin_types: %s' % [origin_types]
        print '\n'
        print 'screen_shot_urls: %s' % [screen_shot_urls]
        print '\n'
        print 'save_time: %s' % save_time
        '''
        result['display_name'] = display_name
        result['icon_url'] = icon_url
        result['color_label'] = color_label
        result['language'] = language
        result['developer'] = developer
        result['star_num'] = star_num
        result['detail_desc'] = detail_desc
        result['short_desc'] = short_desc
        result['origin_types'] = origin_types
        result['screen_shot_urls'] = screen_shot_urls
        result['save_time'] = save_time
        result['game_id'] = game_id
        #result = [display_name, icon_url, color_label, language, developer, star_num, detail_desc, short_desc, origin_types, screen_shot_urls, save_time, game_id]
    return result


def get_tianji():
    conn = connections("45Cursor")
    cursor = conn.cursor()
    sql = """
    SELECT game_id from iplay_tianji_data;
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_gg_need_check_data error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    games = {}
    for row in rows:
        game_id = row[0]
        games[game_id] = ''
    return games
    
 
def get_pkg_info(games):
    conn = connections("GGCursor")
    cursor = conn.cursor()
    sql = """
    SELECT game_id, market_channel, ver_name, file_size, download_url, min_sdk, update_desc, source FROM iplay_game_pkg_info WHERE is_max_version=1 and source in (3, 4) order by gg_download_week desc limit 100;
    """
    rows = None
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
    except Exception as e:
        logger.debug("get_gg_need_check_data error: %s" % str(e.args))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    for row in rows:
        try:
            game_id = row[0]
            if game_id in games:
                continue
            print game_id
            label_info = get_label_info(game_id)
            market_channel = row[1]
            ver_name = row[2]
            file_size = '%.2fM' % (int(row[3])/1024.0/1024)
            download_url = row[4]
            min_sdk = ANDROID[str(int(row[5]))]
            update_desc = row[6] if row[6] else ''
            source = row[7]
            #result = [market_channel, ver_name, file_size, download_url, min_sdk, update_desc]
            label_info['market_channel'] = market_channel
            label_info['ver_name'] = ver_name
            label_info['file_size'] = file_size
            label_info['download_url'] = download_url
            label_info['min_sdk'] = min_sdk
            label_info['update_desc'] = update_desc
            label_info['source'] = source
            insert_data(label_info)
        except:
            logger.debug("ERROR game_id: %s" % str(game_id))

def insert_data(pkg_info):
    conn = connections("45Cursor")
    cursor = conn.cursor()
    sql = """
        INSERT INTO iplay_tianji_data(
        display_name
        , market_channel
        , ver_name
        , file_size
        , download_url
        , icon_url
        , min_sdk
        , perm
        , star_num
        , category
        , language
        , detail_desc
        , update_desc
        , install_desc
        , screen_shot_urls
        , developer
        , color_label
        , short_desc
        , save_time
        , game_id
        , source
        ) VALUES (
        %(display_name)s
        , %(market_channel)s
        , %(ver_name)s
        , %(file_size)s
        , %(download_url)s
        , %(icon_url)s
        , %(min_sdk)s
        , ''
        , %(star_num)s
        , %(origin_types)s
        , %(language)s
        , %(detail_desc)s
        , %(update_desc)s
        , ''
        , %(screen_shot_urls)s
        , %(developer)s
        , %(color_label)s
        , %(short_desc)s
        , %(save_time)s
        , %(game_id)s
        , %(source)s
        ) ON DUPLICATE KEY UPDATE
        save_time = VALUES(save_time)
     """
#    sql = """
#    INSERT INTO iplay_tianji_data(market_channel,ver_name,file_size,download_url,sdk,update_desc,display_name,icon_url,color_label,lang,company,star,desc,short_desc,category,screen_shot_urls,save_time,perm,install_desc,game_id) VALUES (%(market_channel)s, %(ver_name)s, %(file_size)s, %(download_url)s, %(min_sdk)s, %(update_desc)s, %(display_name)s, %(icon_url)s, %(color_label)s, %(language)s, %(developer)s, %(star_num)s, %(detail_desc)s, %(short_desc)s, %(origin_types)s, %(screen_shot_urls)s, %(save_time)s, '', '', %(game_id)s ) ON DUPLICATE KEY UPDATE save_time = VALUES(save_time)
#    """
    try:
        cursor.execute(sql, pkg_info)
        conn.commit()
    except Exception as e:
        logger.debug("game_id: %s error: %s" % (pkg_info['game_id'] ,str(e.args)))
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


games = get_tianji()
print len(games)
get_pkg_info(games)

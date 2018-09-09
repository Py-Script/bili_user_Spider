import requests
import time
import json
import pymysql

from requests.exceptions import ConnectionError

COOKIE = ''

# 连接MySQL
db = pymysql.connect(host='', user='', password='', db='')

MIN = 0


def get_space(mid):
    """
    进入bili用户主页方便下一步动作
    :param mid: 用户ID
    """
    try:
        headers = {
            'Host': 'space.bilibili.com',
            'Referer': 'https://www.bilibili.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Cookie': COOKIE
        }
        url = 'https://space.bilibili.com/' + str(mid)

        req = requests.get(url, headers=headers, timeout=60)
        if req.status_code == 200:
            print('bili用户主页url:{}'.format(url))
            print('成功进入用户主页')
            # 获取用户个人信息
            get_GetINnfo(mid)
        else:
            print('进入bili用户主页失败,code {}'.format(req.status_code))
    except ConnectionError as e:
        print('ConnectionError网络异常', e.args)


def get_GetINnfo(mid):
    """
    获取用户个人信息
    :param mid: 用户ID
    :return: 返回个人信息
    """
    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'space.bilibili.com',
            'Origin': 'https://space.bilibili.com',
            'Referer': 'https://space.bilibili.com/' + str(mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        data = {
            'mid': str(mid)
        }
        url = 'https://space.bilibili.com/ajax/member/GetInfo'

        req = requests.post(url, headers=headers, data=data, timeout=60)
        if req.status_code == 200:
            print('获取用户个人信息成功')
            status = req.json()
            if status.get('data'):
                data = status.get('data')
                regtimez = time.localtime(data.get('regtime'))
                regtime = time.strftime("%Y-%m-%d %H:%M:%S", regtimez)
                result = {
                    'mid': data.get('mid'),
                    'name': data.get('name'),
                    'sex': data.get('sex'),
                    'regtime': regtime,
                    'birthday': data.get('birthday'),
                    'sign': data.get('sign')
                }
                print('用户个人信息:{}'.format(result))
                save_GetINnfo_mysql(result)
        else:
            print('获取用户个人信息失败,code {}'.format(req.status_code))

    except ConnectionError as e:
        print('ConnectionError网络异常', e.args)


def get_myinfo(mid):
    """
    获取用户关注数量和粉丝数量
    :param mid: 用户ID
    :return: 返回关注数量和粉丝数量
    """
    try:
        headers = {
            'Connection': 'keep-alive',
            'Cookie': COOKIE,
            'Host': 'api.bilibili.com',
            'Referer': 'https://space.bilibili.com/' + str(mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/space/myinfo?jsonp=jsonp'
        print('获取用户关注数量和粉丝数量url:{}'.format(url))
        req = requests.get(url, headers=headers, timeout=60)
        if req.status_code == 200:
            status = req.json()
            if status.get('data'):
                data = status.get('data')
                # 粉丝
                follower = data.get('follower')
                # 关注
                following = data.get('following')
                print('关注数量:{}, 粉丝数量:{}'.format(following, follower))
                return follower, following

        else:
            print('get_myinfo url失败 code:{}'.format(req.status_code))
    except ConnectionError as e:
        print('ConnectionError网络异常', e.args)


def get_followings(mid, pn, ps):
    """
    获取关注用户信息
    :param mid: 用户ID
    :param pn: 页数
    :param ps: 每页数量
    """
    try:
        headers = {
            'Connection': 'keep-alive',
            'Cookie': COOKIE,
            'Host': 'api.bilibili.com',
            'Referer': 'https://space.bilibili.com/' + str(mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/relation/followings?vmid=' + \
            str(mid) + '&pn=' + str(pn) + '&ps=' + \
            str(ps) + '&order=desc&jsonp=jsonp'
        print('获取关注用户信息url:{}'.format(url))
        req = requests.get(url, headers=headers, timeout=60)
        if req.status_code == 200:
            code = req.json()
            if code.get('data'):
                glist = code.get('data').get('list')
                for i in glist:
                    result = {
                        'uname': i.get('uname'),
                        'mid': i.get('mid')
                    }
                    print(result)
                    # 得到mid进入用户主页面
                    get_space(result.get('mid'))
                    # 保存关注用户的mid到数据库
                    save_followers_mysql(result)
            else:
                print('限制只访问前5页')

        else:
            print('获取关注用户信息失败 code:{}'.format(req.status_code))

    except ConnectionError as e:
        print('ConnectionError网络异常', e.args)


def get_followers(mid, pn, ps):
    """
    获取粉丝用户信息
    :param mid: 用户ID
    :param pn: 页数
    :param ps: 每页数量
    """
    try:
        headers = {
            'Connection': 'keep-alive',
            'Cookie': COOKIE,
            'Host': 'api.bilibili.com',
            'Referer': 'https://space.bilibili.com/' + str(mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/relation/followers?vmid=' + \
            str(mid) + '&pn=' + str(pn) + '&ps=' + \
            str(ps) + '&order=desc&jsonp=jsonp'
        print('获取粉丝用户信息url:{}'.format(url))
        req = requests.get(url, headers=headers, timeout=60)
        if req.status_code == 200:
            code = req.json()
            if code.get('data'):
                glist = code.get('data').get('list')
                for i in glist:
                    result = {
                        'uname': i.get('uname'),
                        'mid': i.get('mid')
                    }
                    print(result)
                    # 得到mid进入用户主页面
                    get_space(result.get('mid'))
                    # 保存粉丝用户mid到数据库
                    save_followers_mysql(result)
                else:
                    print('限制只访问前5页')

        else:
            print('获取所有粉丝用户信息失败 code:{}'.format(req.status_code))
    except ConnectionError as e:
        print('ConnectionError网络异常', e.args)


def save_followers_mysql(result):
    """
    将关注和粉丝mid保存至mysql
    """
    uname = result.get('uname')
    mid = result.get('mid')
    try:
        with db.cursor() as cursor:
            sql = "SELECT `mid` FROM `list` WHERE `mid`='%s'" % (mid)
            cursor.execute(sql)
            r = cursor.fetchone()
            if r:
                for i in r:
                    ir = i
                if ir == mid:
                    print('数据库已存在该mid {}'.format(r))
            else:
                sql = """INSERT INTO `list` (`mid`, `name`) VALUES (%d, "%s")""" % (mid, uname)
                cursor.execute(sql)
                print('{} 关注粉丝保存到数据库成功'.format(result))
    finally:
        db.commit()


def save_GetINnfo_mysql(result):
    """
    将用户个人信息保存到mysql
    """
    mid = result.get('mid')
    name = result.get('name')
    sex = result.get('sex')
    regtime = result.get('regtime')
    birthday = result.get('birthday')
    sign = result.get('sign')
    try:
        with db.cursor() as cursor:
            sql = "SELECT `mid` FROM `myinfo` WHERE `mid`='%s'" % (mid)
            cursor.execute(sql)
            r = cursor.fetchone()
            if r:
                for i in r:
                    ir = i
                if ir == mid:
                    print('数据库已存在该用户 {}'.format(r))
            else:
                sql = """INSERT INTO `myinfo` (`mid`, `name`, `sex`, `regtime`, `birthday`, `sign`) VALUES (%d, "%s","%s", "%s","%s", "%s")""" % (
                    mid, name, sex, regtime, birthday, pymysql.escape_string(sign))
                cursor.execute(sql)
                print('{} 用户信息保存到数据库成功'.format(result))
    finally:
        db.commit()


def run(mid):
    """
    运行函数
    """

    # 进入用户主页
    get_space(mid)

    # 获取关注数量和粉丝数量
    f, g = get_myinfo(mid)

    # 获取关注用户信息
    f_g_ps = 50
    f_g_pn = int(g / f_g_ps)+1
    if f_g_pn <= 1:
        get_followers(mid, 1, f_g_ps)
    else:
        for g_pn in range(1, f_g_pn):
          get_followings(mid, g_pn, f_g_ps)

    # 获取粉丝用户信息
    f_r_ps = 50
    f_r_pn = int(f / f_r_ps)+1
    print(f_r_pn)
    if f_r_pn <= 1:
        get_followers(mid, 1, f_r_ps)
    else:
        for r_pn in range(1, f_r_pn):
            get_followers(mid, r_pn, f_r_ps)

    # 提取一个mid继续运行
    rep_mid = rep_run()
    if rep_mid:
        return run(rep_mid)


def rep_run():
    """
    当上一个mid所有事情完成后进入此函数进行循环爬取下一个mid
    """
    global MIN
    # 每次运行此函数使MIN加一,不能大于max(数据库count)
    MIN += 1
    cursor = db.cursor()
    # 执行SQL得到COUNT
    sql = "SELECT COUNT(id) FROM `list`"
    cursor.execute(sql)
    r = cursor.fetchone()
    if r:
        for i in r:
            ir = i
        # 判断count是否小于MIN,如果小于则停止程序
        if ir < MIN:
            print('程序即将停止运行,所有信息爬取完成')
            time.sleep(10)
            db.close()
            exit()
        else:
            sql = "SELECT `mid` FROM `list` WHERE id=%d" % (MIN)
            cursor.execute(sql)
            r = cursor.fetchone()
            if r:
                for i in r:
                    return i


if __name__ == '__main__':
    # 最好填写自己的mid
    run(10047741)

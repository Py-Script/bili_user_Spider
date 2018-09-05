import requests
import time
import json

import pymongo




# 连接MongoDB
client = pymongo.MongoClient(host='localhost',port=27017)
db = client.bilibili_user

SESSION = requests.session()
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
            'Cookie': 'inger=edc6ecda; LIVE_BUVID=AUTO2115358816933697; fts=1535889908; sid=hvigwhgz; DedeUserID=10047741; DedeUserID__ckMd5=ece5181ea73c3b76; SESSDATA=5892a772%2C1538481904%2Ca0bf2d94; bili_jct=5dd829ab21ad7d606a04cf0249a29579; stardustvideo=1; CURRENT_FNVAL=8; buvid3=1468A13B-AB50-4895-9697-B514F0F4BC7B6684infoc; rpdid=oloiimsossdosksqlwwqw; _dfcaptcha=bbee0b745b1ea7249886e07bdf1fed68; UM_distinctid=165a3008d49b5-0faf4d2bbdefc2-323b5b03-1fa400-165a3008d4a2bc; CNZZDATA2724999=cnzz_eid%3D418608190-1536036965-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1536036965; im_notify_type_10047741=0; bp_t_offset_10047741=159777945964518621'
        }
        url = 'https://space.bilibili.com/' + str(mid)
        print('bili用户主页url:{}'.format(url))
        req = SESSION.get(url, headers=headers)
        if req.status_code == 200:
            print('成功进入用户主页')
            # 获取用户个人信息
            get_GetINnfo(mid)
            
            
        else:
            print('进入bili用户主页失败,code {}'.format(req.status_code))

    except ConnectionError:
        pass



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

        req = SESSION.post(url, headers=headers, data=data)
        if req.status_code == 200:
            print('获取用户个人信息成功')
            status = req.json()
            if status.get('data'):
                data = status.get('data')
                regtimez = time.localtime(data.get('regtime'))
                regtime=time.strftime("%Y-%m-%d %H:%M:%S", regtimez)
                result = {
                    'mid': data.get('mid'),
                    'name': data.get('name'),
                    'sex': data.get('sex'),
                    'regtime': regtime,
                    'birthday': data.get('birthday'),
                    'sign': data.get('sign')
                }
                print('用户个人信息:{}'.format(result))
                save_GetINnfo_mongodb(result)

        else:
            print('获取用户个人信息失败,code {}'.format(req.status_code))
    
    except ConnectionError:
        pass



def get_myinfo(mid):
    """
    获取用户所有关注数量和粉丝数量
    :param mid: 用户ID
    :return: 返回关注数量和粉丝数量
    """
    try:
        headers = {
            'Connection': 'keep-alive',
            'Cookie': 'inger=edc6ecda; LIVE_BUVID=AUTO2115358816933697; fts=1535889908; sid=hvigwhgz; DedeUserID=10047741; DedeUserID__ckMd5=ece5181ea73c3b76; SESSDATA=5892a772%2C1538481904%2Ca0bf2d94; bili_jct=5dd829ab21ad7d606a04cf0249a29579; stardustvideo=1; CURRENT_FNVAL=8; buvid3=1468A13B-AB50-4895-9697-B514F0F4BC7B6684infoc; rpdid=oloiimsossdosksqlwwqw; _dfcaptcha=bbee0b745b1ea7249886e07bdf1fed68; UM_distinctid=165a3008d49b5-0faf4d2bbdefc2-323b5b03-1fa400-165a3008d4a2bc; CNZZDATA2724999=cnzz_eid%3D418608190-1536036965-https%253A%252F%252Fwww.bilibili.com%252F%26ntime%3D1536036965; im_notify_type_10047741=0; bp_t_offset_10047741=159777945964518621',
            'Host': 'api.bilibili.com',
            'Referer': 'https://space.bilibili.com/' + str(mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/space/myinfo?jsonp=jsonp'
        print('获取用户所有关注数量和粉丝数量url:{}'.format(url))
        req = SESSION.get(url, headers=headers)
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

    except ConnectionError:
        pass


def get_followings(mid, pn, ps):
    """
    获取所有关注用户信息
    :param mid: 用户ID
    :param pn: 页数
    :param ps: 每页数量
    """
    try:
        headers = {
            'Connection': 'keep-alive',
            'Cookie': 'finger=edc6ecda; LIVE_BUVID=AUTO2115358816933697; fts=1535889908; sid=hvigwhgz; DedeUserID=10047741; DedeUserID__ckMd5=ece5181ea73c3b76; SESSDATA=5892a772%2C1538481904%2Ca0bf2d94; bili_jct=5dd829ab21ad7d606a04cf0249a29579; stardustvideo=1; CURRENT_FNVAL=8; buvid3=1468A13B-AB50-4895-9697-B514F0F4BC7B6684infoc; rpdid=oloiimsossdosksqlwwqw; _dfcaptcha=bbee0b745b1ea7249886e07bdf1fed68; UM_distinctid=165a3008d49b5-0faf4d2bbdefc2-323b5b03-1fa400-165a3008d4a2bc; im_notify_type_10047741=0; bp_t_offset_10047741=159777945964518621',
            'Host': 'api.bilibili.com',
            'Referer': 'https://space.bilibili.com/' + str(mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/relation/followings?vmid=' + str(mid) + '&pn=' + str(pn) + '&ps=' + str(ps) + '&order=desc&jsonp=jsonp'
        print('获取所有关注用户信息url:{}'.format(url))
        req = SESSION.get(url, headers=headers)
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
                    get_space(result.get('mid'))
                    #save_followers_json(result)
                    save_followers_mongodb(result)
            else:
                print('限制只访问前5页')
                
        else:
            print('获取所有关注用户信息失败 code:{}'.format(req.status_code))
    
    except ConnectionError:
        pass


def get_followers(mid, pn, ps):
    """
    获取所有粉丝用户信息
    :param mid: 用户ID
    :param pn: 页数
    :param ps: 每页数量
    """
    try:
        headers = {
            'Connection': 'keep-alive',
            'Cookie': 'finger=edc6ecda; LIVE_BUVID=AUTO2115358816933697; fts=1535889908; sid=hvigwhgz; DedeUserID=10047741; DedeUserID__ckMd5=ece5181ea73c3b76; SESSDATA=5892a772%2C1538481904%2Ca0bf2d94; bili_jct=5dd829ab21ad7d606a04cf0249a29579; stardustvideo=1; CURRENT_FNVAL=8; buvid3=1468A13B-AB50-4895-9697-B514F0F4BC7B6684infoc; rpdid=oloiimsossdosksqlwwqw; _dfcaptcha=bbee0b745b1ea7249886e07bdf1fed68; UM_distinctid=165a3008d49b5-0faf4d2bbdefc2-323b5b03-1fa400-165a3008d4a2bc; im_notify_type_10047741=0; bp_t_offset_10047741=159777945964518621',
            'Host': 'api.bilibili.com',
            'Referer': 'https://space.bilibili.com/' + str(mid),
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        url = 'https://api.bilibili.com/x/relation/followers?vmid=' + str(mid) + '&pn=' + str(pn) + '&ps=' + str(ps) + '&order=desc&jsonp=jsonp'
        print('获取所有粉丝用户信息url:{}'.format(url))
        req = SESSION.get(url, headers=headers)
        if req.status_code == 200:
            code = req.json()
            if code.get('data'):
                glist = code.get('data').get('list')
                for i in glist:
                    result = {
                        'uname' : i.get('uname'),
                        'mid' : i.get('mid') 
                    }
                    print(result)
                    get_space(result.get('mid'))
                    #save_followers_json(result)
                    save_followers_mongodb(result)
                else:
                    print('限制只访问前5页')
                
        else:
            print('获取所有粉丝用户信息失败 code:{}'.format(req.status_code))
    
    except ConnectionError:
        pass





def save_followers_mongodb(result):
    """
    将关注和粉丝mid保存至mongodb
    """
    
    collection = db.list
    if collection.find_one({'mid':result.get('mid')}):
        print('{}在数据库已存在'.format(result.get('uname')))
    else:
        collection.insert(result)
        print('{}保存到数据库成功'.format(result.get('uname')))


def save_GetINnfo_mongodb(result):
    """
    将用户个人信息保存到mongodb
    """

    collection = db.myinfo
    if collection.find_one({'mid': result.get('mid')}):
        print('{}用户在数据库已存在'.format(result.get('name')))
    else:
        collection.insert(result)
        print('{}用户保存到数据库成功'.format(result.get('name')))



def run(mid):
    """
    运行函数
    """
    
    # 进入用户主页
    get_space(mid)

    # 获取关注数量和粉丝数量
    f, g = get_myinfo(mid)

    # 获取所有关注用户信息
    f_g_ps = 50
    f_g_pn = int(g / f_g_ps)+1
    if f_g_pn <= 1:
        get_followers(mid, 1, f_g_ps)
    else:
        for g_pn in range(1, f_g_pn):
            get_followings(mid, g_pn, f_g_ps)
    
    # 获取所有粉丝用户信息
    f_r_ps = 50
    f_r_pn = int(f / f_r_ps)+1
    print(f_r_pn)
    if f_r_pn <= 1:
        get_followers(mid, 1, f_r_ps)
    else:
        for r_pn in range(1, f_r_pn): 
            get_followers(mid, r_pn, f_r_ps)

    # 循环
    rep_run()


def rep_run():
    """
    当上一个mid所有事情完成后进入此函数进行循环爬取下一个mid
    """
    global MIN
    # 每次运行此函数使MIN加一,不能大于max(数据库count)
    MIN += 1
    collection = db.list
    # 查询数据库所有数据保存到result
    ran = collection.find({})
    result = []
    for x in ran:
        result.append(x)
    # 最大数
    max = len(result)
    if MIN <= max:
        run(result[MIN].get('mid'))
    else:
        print('程序即将停止运行,所有信息爬取完成')
        time.sleep(10)
        exit()



    
if __name__ == '__main__':
    # 最好填写自己的mid
    run(2)

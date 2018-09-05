"""用户主目录URL
URL = https://space.bilibili.com/10047741/
GET
headers 
    Host: space.bilibili.com
    Referer: https://www.bilibili.com/
    User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36

"""


"""用户订阅标签api
URL = https://space.bilibili.com/ajax/tags/getSubList?mid=10047741
GET
Parameters
    mid:10047741(用户ID)
"""


"""用户投稿api
URL = https://space.bilibili.com/ajax/member/getSubmitVideos?mid=10047741&page=1&pagesize=25
GET
Parameters
    mid:10047741
    page:1
    pagesize:25
"""


"""用户个人信息api
URL = https://space.bilibili.com/ajax/member/GetInfo
POST
Data
    mid:10047741
    csrf: 5dd829ab21ad7d606a04cf0249a29579
"""

"""获取myinfo关注数量粉丝数量api
URL = https://api.bilibili.com/x/space/myinfo?jsonp=jsonp
GET
Parameters
    jsonp: jsonp
    callback: __jp0
"""

"""用户个人粉丝关注数量api
URL = https://api.bilibili.com/x/relation/followers?vmid=10047741&pn=1&ps=20&order=desc&jsonp=jsonp
GET
Parameters
    jsonp:jsonp
    #callback: __jp0 (加上无法打开网页)
"""


"""获取用户所有关注api
URL = https://api.bilibili.com/x/relation/followings?vmid=10047741&pn=1&ps=20&order=desc&jsonp=jsonp
GET
Parameters
    vmid: 10047741
    pn: 1
    ps: 20
    order: desc
    jsonp: jsonp
    #callback: __jp7 (加上无法打开网页)
"""


"""获取用户所有粉丝api
URL = https://api.bilibili.com/x/relation/followers?vmid=10047741&pn=1&ps=20&order=desc&jsonp=jsonp
GET
Parameters
    vmid: 10047741
    pn: 1
    ps: 20
    order: desc
    jsonp: jsonp
    #callback: __jp10 (加上无法打开网页)
"""
# -*- coding: utf-8 -*-
# 使python可以讀取中文

### 抓取的起點與結束點
beginIndex = 100000 #起始點
endIndex = 110000 #結束點,抓到這筆之前的資料

### 設定多少筆存一次，請勿更動，目前決定以1000筆存一次
save_count=1000


### import 區#############################################################################
import os
import time
import json
import copy
import requests
from requests.adapters import HTTPAdapter
rs = requests.session()
rs.mount('https://', HTTPAdapter(max_retries=3)) #設定重試數量


### function(def) 宣告區######################################################################

### 創立資料夾的function########
def mkdir(path):
    if  os.path.exists(path)==False:
        os.makedirs(path)
        print '呼叫mkdir，創立資料夾:',path
# 使用例子：
# pathIs='D://test/'
# mkdir(pathIs)
########################



### 印出字典的key與value########
def PrintKeyValue(dic_in):
    for key, value in dic_in.iteritems() :
        print key,'  :  ', value
########################        

###### 輸出錯誤訊息 #############################
def createLog(log, type1):
    date = time.strftime('%Y%m%d')
    with open('./data/log/%s_%s.txt' % (type1, date), 'a') as f:
        f.write(log+'\n')
###########################################


### 變數宣告區 ##############################################################################

# 抓取現在時間
time_start_to_grab=time.time()
# print type(start_time)
# Python 中 time.time() 回傳一長串float形式的數字，那些數字單位是秒，是從 1970/1/1 00:00:00 開始計算到現在
# 格式化後為Tue May 17 15:44:05 2016的形式
# print  time.asctime( time.localtime(time.time()) )

# 因為要爬愛食記，head內的User-Agent改為自己手機的User-Agent，免得被判定為python程式在爬蟲
# 查詢網址為： http://httpbin.org/get
# 設定requests.get(url, headers=head)中的head
head = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; H30-L02 Build/HonorH30-L02) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"
}

# U2：用戶概況
user_url = 'https://ifoodie.tw/api/user/{0}' 
# U4：粉絲清單
follow_url = 'https://ifoodie.tw/api/follow/?limit={0}&offset={1}&rtn_type=user&target_user_id={2}'
# U6：文章列表
blog_url = 'https://ifoodie.tw/api/user/{0}/blogs/?limit={1}&offset={2}'
# U7_url：收藏清單，會得到U8~U10的id
collect_url = 'https://ifoodie.tw/api/collection/?all=true&user_id={0}' 
# U8,U9,U10：收藏餐廳/推薦餐廳/到訪餐廳
restaurant_url = 'https://ifoodie.tw/api/collection/{0}/blogs/?limit={1}&offset={2}' 

# 字串格式化的使用例子
# user_url2=user_url.format('abc')
# print user_url2
# follow_url2=follow_url.format('aaa','bbb','ccc')
# print follow_url2


### 創立存資料的資料夾 ###
#user爬取存放的資料夾
mkdir('./data/user')
#restaurant爬取後存放的資料夾
mkdir('./data/restaurant')
#blog爬取後存放的資料夾
mkdir('./data/blog')
#發生except之log後存放的資料夾
mkdir('./data/log/')

# 讀檔：使用者清單，已預先抓好，約29萬筆
with open('./data/userlist.json','r') as f:
    userlist = json.load(f)


loop=0
count=0


userlist_select = userlist['users'][beginIndex:endIndex] #抓取範圍
user = {} #最後要輸出的user json
response = [] #各個user字典檔的存放位置
restat = {} #最後要輸出的餐廳 json
restList = [] #各餐廳字典檔的存放位置
blogInfo = {} #最後要輸出的blog json
blogs = [] #各blog字典檔的存放位置





# 依序抓取userlist_select中的id
# Test : 暫時將userlist_select設為
# userlist_select = ["55e513b32756dd75cdcda671"]
# userlist_select = ["562de59a699b6e639b5baa77"]   #跟著羽諾吃喝玩樂去～

for u in userlist_select:
    try:
        res = rs.get(user_url.format(u), headers=head)
        jd = json.loads(res.text, encoding='utf8')
        i = jd['response'] #取得user基本資料，存成字典檔i
        i['_id']=i['id']
        i.pop('id', None)
        i.pop('profile_pic', None)
        i.pop('thumb', None)
        i.pop('cover_url', None)
        i.pop('is_following', None)
        # 另一種刪除法
        # del i[ 'id' ]
        # PrintKeyValue(i)
        
        #抓粉絲名單
        #用i['i_id']來抓粉絲名單
        track = [] #先將list清空，以免抓到上個人的粉絲
        x = 0
        while True: #持續翻頁取得粉絲名單
            try:
                followList = follow_url.format(x+300, x, i['_id'])
                followRes = rs.get(followList, headers=head)
                jdFollow = json.loads(followRes.text, encoding='utf8')
                rf = jdFollow['response']          
                for rfi in rf:
                    track.append(rfi['id'])
            except:
                print "no response"
                createLog(i['_id'], 'user_follower')
            if len(rf) < 300: #最後一頁中斷迴圈
                break
            x += 300
        # print len(track) ,'=',i['follower_cnt'],'?'   #檢查是否有抓到全部的粉絲
        i['fans_id_list'] = track #將粉絲清單存到字典i
        # PrintKeyValue(i)
        x = 0
        blogID = [] #先將list清空，以免抓到上個人的文章
        while True: #持續翻頁取得文章清單
            rb = [] #先將list清空，以免抓到上一頁的文章
            try:
                blogList = blog_url.format(i['_id'], x+300, x)
                blogRes = rs.get(blogList, headers=head)
                jdBlog = json.loads(blogRes.text, encoding='utf8')
                # print jdBlog 
                rb = jdBlog['response']  
                for rbi in rb:
                    blogDict = {}  # 先將list清空，以免抓到上一篇文章
                    try:
                        blogDict['_id'] = rbi['id']
                        blogDict['timestamp'] = time.time()
                        blogDict['date'] = rbi['date']
                        blogDict['url'] = rbi['url']   #部落格文章之原始之完整網址   包含文章代碼
                        blogDict['title'] = rbi['title']
                        blogDict['is_paid'] = rbi['is_paid']
                        blogDict['blog_type'] = rbi['url'].split('/')[2]  #僅抓取使用者帳號與部落格網址，不抓其他資訊
                        blogDict['browse_cnt'] = rbi['stat']['browse_cnt']
                        blogDict['favorite_cnt'] = rbi['stat']['favorite_cnt']
                        blogDict['share_cnt'] = rbi['stat']['share_cnt']
                        blogDict['recommend_cnt'] = rbi['stat']['recommend_cnt']
                        blogDict['restaurant_id'] = rbi['restaurant']['id']
                        blogID.append(blogDict['_id'])  # 原本為restaurant 寫錯???
                        blogs.append(blogDict)   ### 最後存成blogInfo(Final)的字典
                        rbi['restaurant']['_id'] = rbi['restaurant']['id']
                        rbi['restaurant']['timestamp'] = time.time()
                        rbi['restaurant'].pop('id', None)
                        if rbi['restaurant']['_id'] not in [ele['_id'] for ele in restList]:
                            restList.append(rbi['restaurant'])
                            print 'restaurant from blog'
                    except:  #當沒有餐廳資訊時，資料為"restaurant": null
                        print "no restaurant data", rbi['title']
            except:
                print "no response"
                createLog(i['_id'], 'user_blog')
            if len(rb) < 300: #最後一頁中斷迴圈
                break
            x += 300   
    
        # copy 和 deepcopy 不同之處在於 copy 儘會複製當前物件
        # 而 deepcopy 則是若該物件有屬性指向其他物件，則也會一併複製
        i['blog_id_list'] = copy.deepcopy(blogID)
        # PrintKeyValue(i)
        # PrintKeyValue(blogDict)  #看最後一筆blogDict的內容
            # 進入個人收藏頁面
        collectionList = collect_url.format(i['_id'])  
        try: 
            collectRes = rs.get(collectionList, headers=head)
            jdCollection = json.loads(collectRes.text, encoding='utf8')
            rc = jdCollection['response']
            #
            for j in xrange(0, 3): #抓收藏/推薦/到訪
                idList = []
                x = 0
                c = [] # 清空餐廳的清單
                c2 = {}
                while True:
                    rr = []
                    try:
                        restReq = restaurant_url.format(rc[j]['id'], x+300, x)
                        restRes = rs.get(restReq, headers=head)
                        jdRestaurant = json.loads(restRes.text, encoding='utf8')
                        rr = jdRestaurant['response']
                        for rri in rr:
                            try:
                                rri['restaurant']['_id'] = rri['restaurant']['id']
                                rri['restaurant']['timestamp'] = time.time()
                                rri['restaurant'].pop('id', None)
                                c2[rri['id']] = rri['restaurant']['_id']
                                if rri['restaurant']['_id'] not in [ele['_id'] for ele in restList]:
                                    restList.append(rri['restaurant'])  #最後儲存餐廳資料的字典
                                    print 'restaurant from collection'
                            except:
                                print "no restaurant data", rri['title']
                    except:
                        print "no response"
                        createLog(rc[j]['id'], 'collection')
                    
                    if len(rr) < 300:
                        break
                    x += 300
                c.append(c2) #將食記{id:餐廳id} 存進c
                if j == 0:
                    i['collection_blog_list'] = copy.deepcopy(c[0])  #存收藏
                elif j == 1:
                    i['recommendation_blog_list'] = copy.deepcopy(c[0])  #存推薦
                elif j == 2:
                    i['visit_blog_list'] = copy.deepcopy(c[0])  #存到訪
            i['timestamp'] = time.time()
            response.append(i)
            print '%d users in the house' % len(response)
        except:
            print "no response"
    except:
        print "no response"
        createLog(u, 'user')   
#     PrintKeyValue(restList[0])
#     print "================"
#     PrintKeyValue(i)   
        
    count+=1
    if count %save_count==0:               
        user['user'] = response
        restat['restaurant'] = restList
        blogInfo['blog'] = blogs      
        
        file_anme_star=beginIndex+save_count*loop
        file_anme_end=beginIndex+count-1
        
        try:
            with open('./data/user/ifoodUsers_%d_%d.json' % (file_anme_star, file_anme_end), 'w') as f:
                json.dump(user, f)
            with open('./data/restaurant/ifoodRestaurant_%d_%d.json' % (file_anme_star, file_anme_end), 'w') as f:
                json.dump(restat, f)
            with open('./data/blog/ifoodBlog_%d_%d.json' % (file_anme_star, file_anme_end), 'w') as f:
                json.dump(blogInfo, f)
            
            user = {} #最後要輸出的user json
            response = [] #各個user字典檔的存放位置
            restat = {} #最後要輸出的餐廳 json
            restList = [] #各餐廳字典檔的存放位置
            blogInfo = {} #最後要輸出的blog json
            blogs = [] #各blog字典檔的存放位置
            loop+=1
        except:
            print 'Failed'
     
        
    elif u == userlist_select[endIndex-beginIndex-1]:  
        user['user'] = response
        restat['restaurant'] = restList
        blogInfo['blog'] = blogs      
        
        file_anme_star=beginIndex+save_count*loop
        file_anme_end=beginIndex+count-1
        
        try:
            with open('./data/user/ifoodUsers_%d_%d.json' % (file_anme_star, file_anme_end), 'w') as f:
                json.dump(user, f)
            with open('./data/restaurant/ifoodRestaurant_%d_%d.json' % (file_anme_star, file_anme_end), 'w') as f:
                json.dump(restat, f)
            with open('./data/blog/ifoodBlog_%d_%d.json' % (file_anme_star, file_anme_end), 'w') as f:
                json.dump(blogInfo, f)
            loop+=1
        except:
            print 'Failed'
        
        
        
        
        
        
time_end_to_grab = time.time()
print '總共花了 ',time_end_to_grab - time_start_to_grab,' 秒'   
print '總共存了 ',loop,' 組檔案'          
# print '發生 ',exceptCount,' 次 except'     

    








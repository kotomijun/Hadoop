# coding=utf-8
# 使python可以讀取中文

### function(def) 宣告區######################################################################

### 創立資料夾的function########
import os
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



# 因為要爬愛食記，head內的User-Agent改為自己手機的User-Agent，免得被判定為python程式在爬蟲
# 查詢網址為： http://httpbin.org/get
# 設定requests.get(url, headers=head)中的head
head = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 4.4.2; H30-L02 Build/HonorH30-L02) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.89 Mobile Safari/537.36"
}

user_list_url = 'https://ifoodie.tw/api/user/?limit={0}&offset={1}'

limit = 10
offset = 0
s_old=set()
import requests
res = requests.get(user_list_url.format(limit, offset), headers=head)
#print res.text
import json
jd = json.loads(res.text, encoding='utf8')
i = jd['response']   #取得user基本資料，存成字典檔i



# PrintKeyValue(i[0])
# print i[0]

    
    
    

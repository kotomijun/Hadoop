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
import requests
res = requests.get(user_list_url.format(limit, offset), headers=head)
#print res.text
import json
jd = json.loads(res.text, encoding='utf8')
i = jd['response']#取得user基本資料，存成字典檔i

PrintKeyValue(i[0])
# print i[0]

# a={'a1':1,'a2':2}
# b={'a1':1,'a2':2}
#   
# import csv  
# with open('./data/names.csv', 'w') as csvfile:
#     fieldnames = ['a1', 'a2']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     writer.writerow(a)
#     writer.writerow(b)
    


# writer = csv.writer(open('./data/dict.csv', 'w'))
# for key, value in i[0].items():
#     writer.writerow([key, value])
    

# rows = [{'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
#         {'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
#         {'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
#         {'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'},
#         {'Column1': '0', 'Column2': '1', 'Column3': '2', 'Column4': '3'}]
# 
# import csv
# 
# fieldnames = ['Column1', 'Column2', 'Column3', 'Column4']
# dict_writer = csv.DictWriter(file('./data/names.csv', 'wb'), fieldnames=fieldnames)
# 
# 
# dict_writer.writerow(fieldnames)      # CSV第一行需要自己加入
# dict_writer.writerows(rows)       # rows就是表單提交的數據

# 
# import csv
# test_array = []
# test_array.append({'fruit': 'apple', 'quantity': 5, 'color': 'red'});
# test_array.append({'fruit': 'pear', 'quantity': 8, 'color': 'green'});
# test_array.append({'fruit': 'banana', 'quantity': 3, 'color': 'yellow'});
# test_array.append({'fruit': 'orange', 'quantity': 11, 'color': 'orange'});
# fieldnames = ['fruit', 'quantity', 'color']
# test_file = open('./data/test2.csv','wb')
# csvwriter = csv.DictWriter(test_file, delimiter=',', fieldnames=fieldnames)
# csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
# for row in test_array:
#     csvwriter.writerow(row)
# test_file.close()  
#    
#    
#    



import csv
fieldnames = ['fav_cnt','profile_pic','follower_cnt','display_name','thumb','following_cnt','post_cnt','cover_url','profile_pic_origin','browse_cnt','checkin_cnt','is_following','id','certified',]
test_file = open('./data/test2.csv','wb')
csvwriter = csv.DictWriter(test_file, delimiter=',', fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for row in i:
    csvwriter.writerow(row)
test_file.close()  
    
    
    
    

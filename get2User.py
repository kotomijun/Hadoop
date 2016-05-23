# coding=utf-8
# 愛食記-User的資料
# https://ifoodie.tw/api/user/?limit=10&offset=0
import requests
url='https://ifoodie.tw/api/user/?limit=2&offset=0'
res = requests.get(url)
# print res
# print res.text
if res.status_code==200:
    print "200 OK,請求已成功"


# 發生UnicodeEncodeError: 'ascii' codec can't encode characters in position 152-156: ordinal not in range(128)
# 加入encode('utf-8')處理，將字串轉為utf-8
resText = res.text.encode('utf-8').replace('"info": {}, ', '').replace(', "success": true','').replace('"id":','"_id":')
# 確定字串的型態是否為utf-8
# print isinstance(resText, 'utf-8')


# 檢查資料預計存取的資料夾，如不存在，創立
import os
document = 'D://Dropbox/Big_data_develop_class/ETL/Workspace/ClassPratice/ifoodie/data/'
if  os.path.exists(document)==False:
    os.makedirs(document) 

# 檔案存取的名稱
dataname = url.split('?')[-1].replace('=','').replace('&','_') 
with open(document+'/'+dataname+'.json', 'w') as f:
    f.write(resText)   
print "資料",dataname,"已儲存於資料夾",document      

# 
# import json
# with open(document+'NewFile.json', 'w') as f:
#     json.dump(resText, f )


         

        
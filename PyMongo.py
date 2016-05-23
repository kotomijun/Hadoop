# coding=utf-8
# 使python可以讀取中文

### function(def) 宣告區######################################################################

### json資料讀取####### 
import json  
def read_json(path):
    with open(path, 'r') as f:
        return  json.load(f)
##################

### 使用pymongo將資料insert進mongodb####
from pymongo import MongoClient
def export_mongodb(collection_name,data):
    connection = MongoClient("localhost", 27017)
    db = connection["db1"]
    db.authenticate("ab101", "1234")
    collection =db[collection_name]
    collection.insert(data)
###############################





### Main###############################################################################
# #ifoodUsers
# data_in=read_json('./data/user/ifoodUsers_0_1.json')
# export_mongodb("ifoodUsers",data_in['user'])
# 
# #ifoodRestaurant
# data_in=read_json('./data/restaurant/ifoodRestaurant_0_1.json')
# export_mongodb("ifoodRestaurant",data_in['restaurant'])
# 
# #ifoodBlog
# data_in=read_json('./data/blog/ifoodBlog_0_1.json')
# export_mongodb("ifoodBlog",data_in['blog'])

#ifoodUsers
data_in=read_json('./data/user/ifoodUsers_0_10.json')
export_mongodb("ifoodUsers",data_in['user'])

#ifoodRestaurant
data_in=read_json('./data/restaurant/ifoodRestaurant_0_10.json')
export_mongodb("ifoodRestaurant",data_in['restaurant'])
 
#ifoodBlog
data_in=read_json('./data/blog/ifoodBlog_0_10.json')
export_mongodb("ifoodBlog",data_in['blog'])





### 範例
# from pymongo import MongoClient
# connection = MongoClient("localhost", 27017)
# db = connection["db1"]
# db.authenticate("ab101", "1234")
# collection = db.books
# book = {
# "_id" : 5.0,
# "isbn" : "0131002872",
# "title" : "Thinking in Java",
# "releaseDate" : "2002-12-01",
# "listPrice" : 100.99,
# "pubId" : "PH"
# }
# collection.insert(book)




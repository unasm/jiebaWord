# -*- coding:utf-8 -*- 

# 显示某个文章里面的词频


AID = 5707

import MySQLdb as mysql
import db

sql = "SELECT * FROM article where id  = %d" % AID;
article = db.getOne(sql)
print "title is : ",  article[1]
print "href is : " , article[2]

sql = "SELECT * FROM track_key WHERE article_id = %d" % AID
#print sql
keys = db.GetList(sql)

cntData = {}
for row in  keys:
    word = row[1]
    #print row
    if not cntData.has_key(word):
        cntData[word] = 0
    cntData[word] = cntData[word] + row[2]
#print type(keys)


result = sorted(cntData.iteritems(), key = lambda asd:asd[1], reverse = True)

cnt = 0
for row in result:
    print row[0], " \t\t", row[1] 
    cnt = cnt + 1
    if cnt > 20:
        break

# -*- coding:utf-8 -*-
import MySQLdb as mysql
import db
import datetime

conn = db.getConn()

def Insert(count, word, article_id):
    nowTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    keys = [
        "word",
        "count",
        "article_id",
        "update_time",
        "insert_time",
    ]  
    dataObj = (
        word,
        count,
        article_id,
        nowTime, 
        nowTime,
    )
    dayTime = datetime.datetime.now().strftime("%Y-%m-%d 00:00:00")
    sql = "select * from track_key where `word` = '%s' && `update_time` >= '%s'&& `article_id` = %d" % (word.encode('utf-8'), dayTime, article_id)
    oldData = db.getOne(sql)
    if oldData == None:
        #每个单词每天只能插入一次
        db.Insert(keys, dataObj, "track_key")

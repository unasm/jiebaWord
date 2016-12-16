# -*- coding:utf-8 -*-
# 从网站抓取数据
import urllib2
import datetime
import re
import simplejson as json
#import json
from bs4 import BeautifulSoup as Domer
import MySQLdb as mysql
import time
import db

timeFormat = "%Y-%m-%d %H:%M:%S"

# 获取一行tr的数据
def parserNews(content):
    try: 
        soup = Domer(content, "html.parser")
        body = soup.find(id="ContentBody")
        news = body.find_all(class_="newsContent", limit=2)
        if len(news) != 1:
            return ''
        return news[0].get_text()
    except Exception, ex: 
        print Exception,":", ex
    return ''
def getUnParseData():
    dataArr = db.GetList("select * from article where status = 0 limit 1")
    for data in dataArr:
        #print data[5]
        parser(data[5])
getUnParseData()
        

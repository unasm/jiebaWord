# -*- coding:utf-8 -*- 

from bs4 import BeautifulSoup as Domer
import matplotlib.pyplot as plt  
import MySQLdb 
import db
import sys
import pandas as pd 
import numpy as np

reload(sys)
sys.setdefaultencoding('utf-8') 

sql = "select title, content from article  limit 1000"
dbDf = pd.read_sql(sql, con=db.conn)
prefix = "/Users/tianyi/project/jieba/proj/td_idf/data"
#for idx in dbDf.index:
path = prefix + "/ldaTest.txt"
fp = open(path, "w")

def parserNews(content):
    try: 
        soup = Domer(content, "html.parser")
        body = soup.find(id="ContentBody")
        if body == None:
            print "wrong type whthout contentBody"
            return ''
        news = body.find_all(class_="newsContent", limit=2)
        if len(news) != 1:
            return ''
        return news[0].get_text()
    except Exception, ex: 
        print Exception,":", ex
    return ''

for idx in range(0, dbDf.shape[0]):
    #print idx
    row = dbDf.loc[idx]
    #print row
    #print path
    fp.write(row['title'] )
    content = parserNews(row['content']) + "\r\n"
    fp.write(content)
    #break


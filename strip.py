# -*- coding:utf-8 -*-
# 从网站抓取数据
import sys
sys.path.append("../")

from bs4 import BeautifulSoup as Domer
import MySQLdb as mysql
import db
import dbIgnore
import dbTrace
import re
import jieba
import jieba.posseg
import jieba.analyse

timeFormat = "%Y-%m-%d %H:%M:%S"

# 获取一行tr的数据
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
def processData(dataArr, blackData):
    jieba.load_userdict('/Users/tianyi/project/jieba/proj/new_dict.txt')
    pattern = re.compile(r'^\d+$')
    for data in dataArr:
        print "cutting : " , data[0]
        #print data[5]
        news = parserNews(data[5])
        #print type(seg_list)
        #seg_list = jieba.cut(news)
        # 能够匹配出来，动车，动车组，车组三种
        seg_list = jieba.cut(news, cut_all=True)
        #seg_list = jieba.posseg.cut(news)
        #cnt = 0
        segs = []
        for seg in seg_list:
            #print seg.word, seg.flag,带有情感的词
            if len(seg) <= 1:
                continue
            #整数过滤掉
            if pattern.match(seg):
                continue
            segs.append(seg)
            #print seg, len(seg), type(seg)
        survive = list(set(segs).difference(set(blackData)))
        for word in survive:
            cnt = 0
            for seg in segs:
                if word == seg:
                    cnt = cnt + 1
            where = {"article_id" : data[0], "word" : word}
            #print where
            row = db.get(where, 'track_key')
            if not row:
                print word
                dbTrace.Insert(cnt, word, data[0])
def getUnParseData():
    dataArr = db.GetList("select * from article where status = 0")
    #dataArr = db.GetList("select * from article where status = 0 limit 1")
    blackData =  dbIgnore.getBlacks()
    processData(dataArr, blackData) 
getUnParseData()

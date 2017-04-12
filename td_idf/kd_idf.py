# -*- coding:utf-8 -*- 

import matplotlib.pyplot as plt  
import MySQLdb 
import db
import sys
import pandas as pd 
import numpy as np

THRESHOLD_RATE = 0.05

#sql = "select * from ignore_key where `is_delete` = 0"
#sql = "select distinct article_id from ignore_key where `is_delete` = 0"
#arr = db.GetList(sql)
sql = "select track_key.*, word_attr.flag from track_key left join word_attr on track_key.word = \
            word_attr.word where is_delete = 0 and word_attr.flag in('n', 'nz', 'nr', 'nrt', 'ns', 'nt', 'nrfg', 'ng') \
            "
if len(sys.argv) >= 2 and sys.argv[1] == 'test' :
    sql = "select track_key.*, word_attr.flag from track_key left join word_attr on track_key.word = \
        word_attr.word where is_delete = 0 and word_attr.flag in('n', 'nz', 'nr', 'nrt', 'ns', 'nt', 'nrfg', 'ng') \
        and article_id < 100 limit 100"
dbDf = pd.read_sql(sql, con=db.conn)
            #and article_id < 100 limit 100", con=db.conn)
#dbDf = pd.read_sql("select track_key.*, word_attr.flag from track_key left join word_attr on track_key.word = word_attr.word where is_delete  = 0  order by article_id limit 100", con=db.conn)
#dbDf = pd.read_sql("select * from track_key where `is_delete` = 0 limit 10000", con=db.conn)
#artIds = dbDf.filter(items=['article_id']).diff()
# show times in article

def getWordCnt(obj):
    
    return obj.count()[0]

wordArtCnt = dbDf.groupby('word').apply(getWordCnt)

def getArtCnt(obj):
    #返回每个的统计信息
    #print obj['word']
    #print type(obj)
    for idx in obj.index:
        #print idx
        #该单词在文档的数量,如果单词在太多的文章里面出现，就是一个普遍意义的词，而非表征特性的词
        # 越有意义的词，在被使用的文章越少，单个文章中被使用的越多
        row = obj.loc[idx]
        artNum = wordArtCnt.get(row.word)
        #row.weight = row["count"] / artNum
        #obj.loc[idx]["weight"] = float(row["count"] / artNum)
        obj.set_value(idx, 'weight', float(row["count"]) / float(artNum))
        #obj.set_value(idx, 'weight', float(row["count"]) / float(artNum * totalWord))
    sortList = obj.sort_values("weight", axis = 0, ascending = False)[:5]
    for idx in sortList.index:
        val = sortList.loc[idx]
        print val['word'], "\t", val['article_id'], "\t", val['weight'], "\t", val['count']
        #print sortList.loc[idx]["weight"], 
    print ""
    #print type(sortList)
    #for  val in sortList:
    #    print val
    #print sortList
    return {"count" : obj.count()[0], "sum" : obj["count"].sum(), 'maxCount' : obj['count'].max(), 'freq' : 0.0}

def showBar(freqArr):
    width = 0.1
    ind = np.linspace(0.5, 19.5, len(freqArr))
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    values = freqArr.values()
    ax.bar(ind-width/2, values, width, color = "green")
    ax.set_xticks(ind)
    ax.set_xlabel('items')
    ax.set_ylabel('values')
    plt.grid(True)
    plt.show()
def addFreq(artIds):
    freqArr = {}
    for idx in artIds.index:
        row = artIds.get(idx)
        #print row
        freqArr[idx] = float(row['maxCount']) / float(row['sum']) 
        row['freq'] = float(row['maxCount']) / float(row['sum']) 
    return freqArr
    #return {"count" : obj.count()[0]}
def dispSortWord(words):
    for idx in words.index:
        print idx, "\t",words.get(idx)

# 过滤掉过滤掉那些只小于threshold的单词, 很偏僻的词，或者从来没有人关注过的东西
# @words        单词的列表
# @threshold    过滤的阈值
def dropWords(words, threshold):
    for idx in words.index:
        cnt = words.get(idx)
        if cnt < threshold:
            print cnt, idx
            words.pop(idx)
artIds = dbDf.groupby('article_id').apply(getArtCnt)

#freqArr = dict(sorted(freqArr.iteritems(), key = lambda val: val[1], reverse = True))
#showBar(freqArr)

#totalArtNum = artIds.shape[0]

#dispSortWord(wordArtCnt)
#print wordArtCnt.le(int(totalArtNum * 0.05))
#sortWord = wordArtCnt.sort_values(axis=0, ascending=False)

#dropWords(wordArtCnt, 2)
#cnt = 1
#for idx in range(0, dbDf.shape[0]):
#    row = dbDf.loc[idx]
#    # 高频无意义单词
#    if wordArtCnt.get(row['word']) == None:
#        continue
#    #print row
#    #获得该文章的单词总数
#    wordNum = artIds.get(row.article_id)['sum']
#    print row["count"]
#    print float(float(row["count"]) / float(wordNum))
#    cnt -= 1
#    if cnt < 0:
#        break

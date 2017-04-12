# -*- coding:utf-8 -*- 

import matplotlib.pyplot as plt  
import MySQLdb 
import db
import pandas as pd 
import numpy as np

THRESHOLD_RATE = 0.05

#sql = "select * from ignore_key where `is_delete` = 0"
#sql = "select distinct article_id from ignore_key where `is_delete` = 0"
#arr = db.GetList(sql)
dbDf = pd.read_sql("select track_key.*, word_attr.flag from track_key left join word_attr on track_key.word = \
            word_attr.word where is_delete = 0 and word_attr.flag in('n', 'nz', 'nr', 'nrt', 'ns', 'nt', 'nrfg', 'ng') \
            ", con=db.conn)
            #and article_id < 100 limit 100", con=db.conn)
#dbDf = pd.read_sql("select track_key.*, word_attr.flag from track_key left join word_attr on track_key.word = word_attr.word where is_delete  = 0  order by article_id limit 100", con=db.conn)
#dbDf = pd.read_sql("select * from track_key where `is_delete` = 0 limit 10000", con=db.conn)
#artIds = dbDf.filter(items=['article_id']).diff()
def getArtCnt(obj):
    #返回每个的统计信息
    #print obj['word']
    return {"count" : obj.count()[0], "sum" : obj["count"].sum(), 'maxCount' : obj['count'].max(), 'freq' : 0.0 }

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

def getWordCnt(obj):
    #该单词在文档的数量
    return obj.count()[0]
    #return {"count" : obj.count()[0]}
def dispSortWord(words):
    for idx in words.index:
        print idx, "\t",words.get(idx)

# 过滤掉那些出现频率过高的单词，因为没有意义
# @words        单词的列表
# @threshold    过滤的阈值
def dropWords(words, threshold):
    for idx in words.index:
        cnt = words.get(idx)
        #这些单词，出现在太多的文档里面了
        if cnt > threshold:
            #print words.shape, cnt, idx
            words.pop(idx)
            delWowrd(idx)
            #print idx
def delWowrd(word):
    nodeArr = [
       'is_delete',
    ]
    dataObj = (
        #datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        1,
    )
    db.update(nodeArr, dataObj, {'word' : word}, 'track_key')
artIds = dbDf.groupby('article_id').apply(getArtCnt)

# 过滤掉过滤掉那些只小于threshold的单词, 很偏僻的词，或者从来没有人关注过的东西
# @words        单词的列表
# @threshold    过滤的阈值
def dropLessWords(words, threshold):
    for idx in words.index:
        cnt = words.get(idx)
        if cnt < threshold:
            #print cnt, idx
            words.pop(idx)
            delWowrd(idx)

#freqArr = dict(sorted(freqArr.iteritems(), key = lambda val: val[1], reverse = True))
#showBar(freqArr)



#totalArtNum = artIds.shape[0]
#print totalArtNum
wordArtCnt = dbDf.groupby('word').apply(getWordCnt)
#print wordArtCnt.le(int(totalArtNum * 0.05))
#sortWord = wordArtCnt.sort_values(axis=0, ascending=False)

dropWords(wordArtCnt, int(artIds.shape[0] * THRESHOLD_RATE))
dropLessWords(wordArtCnt, 2)

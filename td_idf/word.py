# -*- coding:utf-8 -*- 

#  通过tf_idf 的思想获取 某一天的 关键性的名词

import matplotlib.pyplot as plt  
import MySQLdb 
import db
import datetime
import sys
import pandas as pd 
import numpy as np

#sql = "select * from ignore_key where `is_delete` = 0"
#sql = "select distinct article_id from ignore_key where `is_delete` = 0"
#arr = db.GetList(sql)
class Word:

    #名次的数组
    NounArr = ['n', 'nz', 'nr', 'nrt', 'nt', 'nrfg', 'ng', 'j']
    #动词的列表
    VecArr = ['vd', 'vd', 'vg', 'vi', 'vn', 'vq']

    targetFlag = VecArr
    __isTest = True
    __topWordNum = 10
    #if len(sys.argv) >= 3 and sys.argv[2] == 'nonu' :

    #nowTime = datetime.datetime.now()
    #nowTime = datetime.date(2016,  12, 15)  
    #timeStart = nowTime.strftime('%Y-%m-%d 00:00:00')
    #delta = datetime.timedelta(days=1)
    #endTime = delta + nowTime
    #timeEnd = endTime.strftime('%Y-%m-%d 00:00:00')

    def getArtIds(self, timeStart, timeEnd):
        sql = "select id from article where release_time >= '%s' and release_time <= '%s'" % (timeStart, timeEnd)
        if self.__isTest == True:
            sql = "select id from article where release_time >= '%s' and release_time <= '%s' limit 10" % (timeStart, timeEnd)
        dbDf = pd.read_sql(sql, con=db.conn)
        #print dbDf['id']
        idList = []
        for val in dbDf['id'].values:
            idList.append(str(val))
        return idList

    #获取 查询 单词的 sql
    def getSql(self, artIdArr):
        targetFlag = self.NounArr
        sql = "select track_key.*, word_attr.flag from track_key left join word_attr on track_key.word = \
                    word_attr.word where is_delete = 0 and word_attr.flag in('%s') \
                    and is_delete = 0 and article_id in('%s')" % ("','".join(targetFlag), "','".join(artIdArr))
       # if len(sys.argv) >= 2 and sys.argv[1] == 'test' :
        if self.__isTest == True:
            sql = "select track_key.*, word_attr.flag from track_key left join word_attr on track_key.word = \
                word_attr.word where is_delete = 0 and word_attr.flag in('%s') \
                and is_delete = 0 and article_id in('%s') limit 10" % ("','".join(targetFlag), "','".join(artIdArr))
        return sql

    #每个单词 出现在的文章数
    def getWordCnt(self, obj):
        val = obj.count()[0]
        if val > 500:
            val = 500
        return val


    #每个单词在所有文章中出现的总数
    def getWordCntTotalGrp(self, obj):
        return obj["count"].sum()

    def getArtCnt(self, obj):
        return {"count" : obj.count()[0], "sum" : obj["count"].sum(), 'maxCount' : obj['count'].max(), 'freq' : 0.0}
    #disp 图片
    def showBar(self, freqArr):
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
    def dropWords(self, words, threshold):
        for idx in words.index:
            cnt = words.get(idx)
            if cnt < threshold:
                #print cnt, idx
                words.pop(idx)

    def getCntRange(self, obj):
        return obj.count()[0]

    #获取topN的单词
    def getTopN(self, obj):
        for idx in obj.index:
            #该单词在文档的数量,如果单词在太多的文章里面出现，就是一个普遍意义的词，而非表征特性的词
            # 越有意义的词，在被使用的文章越少，单个文章中被使用的越多
            row = obj.loc[idx]
            artNum = self.wordArtCnt.get(row.word)
            totalWordNum = self.wordArtCntTotal.get(row.word)

            obj.set_value(idx, 'weight', 0.0)
            obj.set_value(idx, 'freqCoff', 0.0)
            obj.set_value(idx, 'selfFreq', 0.0)
            if artNum > (0.1 * self.totalArtNum):
                #在太多文章中出现的单词没有意义
                continue
            #文章系数， sin(极限值) ，那 1/2 的极限值是系数最大的，最想要的词系数尽可能大
            coff = np.sin(float(artNum) / (0.1 * float(self.totalArtNum) * np.pi))
            # 前面 前面部分为系数，表征的是 单词相对于自己来说，在该文章中出现的频率
            # 后者表征的是同一篇文章出现的多的应该是更重要的单词, 但是是否需要避免过度倾向出现频率过高的单词
            maxCount = float(row['count'])
            if maxCount > 9.0:
                maxCount = 9.0
            avageCoff = (float(row["count"] * artNum) / float(totalWordNum)) * np.exp(maxCount / 2.0)
            obj.set_value(idx, 'weight', coff * avageCoff)
            obj.set_value(idx, 'freqCoff', coff)
            obj.set_value(idx, 'selfFreq', avageCoff)
        sortList = obj.sort_values("weight", axis = 0, ascending = False)[:self.__topWordNum]
        reList = []
        for idx in sortList.index:
            val = sortList.loc[idx]
            row = {
                "word": val['word'], 
                #单词在文章中出现的次数
                "count" : val['count'], 
                #单词的计算权重
                'weight' : val['weight'], 
                'freqCoff' : val['freqCoff'], 
                'selfFreq' : val['selfFreq'], 
                #出现在的文章数
                'wordArtCnt' : self.wordArtCnt.get(row["word"]),
                #artId
                'artId' : val['article_id'],
                'flag' : val['flag']
            }
            reList.append(row)
        return reList
    # 返回某个单词的top N 列表, 如果没有artId ，则默认是全部
    #print self.artTopN.get(9293)
    def getArtTopN(self, artId = -1):
        if artId == -1:
            return self.artTopN
        return self.artTopN.get(artId)

    def __init__(self, timeStart, timeEnd):
        #每个单词的出现总数
        sql = self.getSql(self.getArtIds(timeStart, timeEnd))
        #从数据库拿到的数据集合
        self.dbDf = pd.read_sql(sql, con=db.conn)
        self.wordArtCntTotal = self.dbDf.groupby('word').apply(self.getWordCntTotalGrp)
        #每个单词出现在的文章数
        self.wordArtCnt = dict(self.dbDf.groupby('word').apply(self.getWordCnt))
        self.totalArtNum = self.dbDf.groupby('article_id').apply(self.getArtCnt).count()
        #获得每个单词的topN 个单词
        self.artTopN = self.dbDf.groupby('article_id').apply(self.getTopN)

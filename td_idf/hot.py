# -*- coding:utf-8 -*- 

from gensim import corpora, models, similarities
import gensim
import matplotlib.pyplot as plt  
from networkx.drawing.nx_agraph import graphviz_layout
import datetime
import networkx as nx
import MySQLdb 
import db
import sys
import re
#import word
import pandas as pd 
import numpy as np

#G = nx.Graph()
class Hot:
    # 单词与 id 之间的映射关系
    dictMap = {}
    #id 到单词之间的映射
    dictMapRev = {}
    idxCnt = 0
    #通过词之间绘制的词图
    edgeMap = {}
    # @topKeys      通过Word  切词 分成的
    def makeMap(self, topWords):
        edgeMap = {}
        for rows in topWords:
            lastPoints = []
            for row in rows:
                if not self.dictMap.has_key(row['word']):
                    self.dictMap[row['word']] = self.idxCnt
                    edgeMap[self.idxCnt] = {}
                    self.dictMapRev[self.idxCnt] = row['word']
                    self.idxCnt += 1

                nowPoint = self.dictMap[row['word']]
                for point in lastPoints:
                    if not edgeMap[point].has_key(nowPoint):
                        edgeMap[point][nowPoint] = 0

                    if not edgeMap[nowPoint].has_key(point):
                        edgeMap[nowPoint][point] = 0
                    if nowPoint == point :
                        print "repeat", nowPoint, point
                    edgeMap[nowPoint][point] += 1
                    edgeMap[point][nowPoint] += 1
                lastPoints.append(nowPoint)
        return edgeMap
    #@idxCnt 最大的idx
    def getPR(self, idxCnt, edgeMap):
        
        outWeight = {}
        pR = {}
        pR_t = {}
        #最大迭代次数，防止死循环
        maxRepeat = 1000
        maxDiff = 0.0001
        #初始化pr值 和weight
        for idx in range(0, idxCnt):
            pR[idx] = 1.0
            #存在一条边都没的情况
            if edgeMap.has_key(idx):
                outWeight[idx] = float(sum(edgeMap[idx].values()))
            else:
                outWeight[idx] = 0
                pR[idx] = 0.0
        while(maxRepeat > 0):
            isRepeat = False
            for idx in range(0, idxCnt):
                # 计算单个节点的pR值
                pR_t[idx] = 0.0
                if edgeMap.has_key(idx):
                    for node in edgeMap[idx]:
                        pR_t[idx] += pR[node] *  (edgeMap[idx][node] / (outWeight[node] + 1))
                    pR_t[idx] = pR_t[idx] * 0.85 + 0.15
            for idx in range(0, idxCnt):
                diff = pR_t[idx] - pR[idx]
                if diff > maxDiff or diff < -maxDiff:
                    maxRepeat -= 1
                    isRepeat = True
                    break
            if isRepeat == False:
                break
            pR = pR_t
        return pR
    def sortPr(self, pr):
        val = []
        for idx in range(0, len(pr)):
            val.append((idx, pr[idx]))
        return sorted(val, key = lambda val: val[1], reverse=True)
    def dispTopPr(self, numbers = 10):
        for idx in range(0, min(numbers, len(self.sortPRList))):
            row = self.sortPRList[idx]
            if len(self.dictMapRev[row[0]].strip()) <= 9:
                print ("%s \t\t %.2f\t\t %s" % (self.dictMapRev[row[0]], row[1], sum(self.edgeMap[row[0]].values())))
            else:
                print ("%s \t %.2f\t\t %s" % (self.dictMapRev[row[0]], row[1], sum(self.edgeMap[row[0]].values())))
    
    def __init__(self, wordsLine , numbers = 30):
        self.edgeMap = self.makeMap(wordsLine)
        pR = self.getPR(self.idxCnt, self.edgeMap)
        self.sortPRList = self.sortPr(pR)

    #doclist = docs.values
    #texts = [[word for word in doc.lower().split() if word not in stoplist] for doc in doclist]
    #print len(texts)
    #print texts[0]
    #dictionary = corpora.Dictionary(texts)
    #corpus = [dictionary.doc2bow(text) for text in texts]
    ##print corpus[13]
    #lda = gensim.models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=20)
    #print lda.print_topic(10, topn=5)

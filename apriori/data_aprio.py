# -*- coding:utf-8 -*- 

import sys
sys.path.append("../lib")

import db
import pandas as pd
import datetime as dtime
from numba import vectorize
from numba import jit
from numba import guvectorize
import time
import numpy as np
import colour
#from lib import colour

class StockApori:
    __supportData = {}
    __TEST = False
    __FILEDATA = True
    __filePath = "/Users/tianyi/project/jieba/proj/data/aprodata.csv"

    #两组数据之间最小的支持度

    __minConf = 0.7
    def getDataCount(self, dbDf):
        #获取数据的天数
        if not self.dataCount:
            self.dataCount = dbDf.apply(getDays).groupby("day").count()
        return self.dataCount

    def markDay(self, obj):
        return time.strftime("%Y%m%d", time.localtime(obj))

    def getData(self):
        if not self.__FILEDATA:
            startTime = dtime.datetime.strptime("20140101", "%Y%m%d") 
            #startTime = dtime.datetime.now()
            endTime  = dtime.timedelta(days=40) + startTime
            dataSql = "select percent, time, code from history where time >= '%d' and time <= '%d'" % (
                int(time.mktime(startTime.timetuple())) , int(time.mktime(endTime.timetuple())))
            print dataSql
            if self.__TEST:
                dataSql = "select percent, time, code from history where time >= '%d' and time <= '%d' limit 100" % (
                    int(time.mktime(startTime.timetuple())) , int(time.mktime(endTime.timetuple())))
            dbDf = pd.read_sql(dataSql, con = db.conn)
        else:
            headerArr = ['percent', 'time', 'code']
            dbDf = pd.read_csv(self.__filePath, sep="\t",names = headerArr)
        #print dataSql
        #print dbDf.shape
        #print dbDf.head()
        #一天为单位 获取数据
        #dbDf = dbDf.sort_values('time', axis=0, ascending=True)
        # 标记日子
        self.__dbDf = dbDf
        dbDf['day'] = dbDf['time'].apply(self.markDay)
        # 获取
        self.__riseData = dbDf[dbDf.percent > 0]
        #print self.__riseData.head()
        self.__downData = dbDf[dbDf.percent < 0]
        #print self.__downData.shape

    def rulesFromSeq(self, freqSeq, Ck, support):
        m = len(Ck[0])
        res = {}
        if (len(freqSeq) > m + 1):
            cand = self.aporiGen(Ck, m + 1)
            res = self.calConf(freqSeq, cand, support)
            #print res
            if len(cand) > 1:
                tmp = self.rulesFromSeq(freqSeq, cand, support)
                res.update(tmp)
            return res
        return {}


    def aporiGen(self, data, length):
        """
            从候选的频繁集项里面，组成新的频繁集项
        """
        retList = []
        #print type(data)
        #print data
        #print data.shape()
        lenData = len(data)
        #print data
        for i in range(lenData):
            for j in range(i+1, lenData):
                #print data[i]
                L1 = list(data[i])[:length - 2]
                L2 = list(data[j])[:length - 2]
                #L1.sort()
                #L2.sort()
                if L1 == L2:
                    #print type(data[i])
                    retList.append(data[i] | data[j])
        return retList

    def calConf(self, freqSeq, Ck, support):
        """
            获取最小支持度
        """
        result = {}
        for can in Ck:
            conf = support[freqSeq] / support[freqSeq - can]
            if self.__minConf < conf:
                # 当freqSeq - can 出现的时候，freqSet 出现的频率
                result[freqSeq - can] = (can, conf)
                #result.append((freqSet - can, can, conf))
        return result

    def createSet(self, data):
        """
            根据data数据创 C1
        """
        C1 = []
        for row in data:
            #print row
            for col in row:
                #print col
                if not [col] in C1:
                    C1.append([col])
        C1.sort()
        return map(frozenset, C1)

    def getEachDay(self, obj):
        return obj['code'].get_values()

    def formatData(self, data):
        # 将数据整理成 二维数组的形式
        C1 = {}
        C1Idx = -1;
        lastDay = -1
        #data = data.sort_values('day', axis = 0, ascending = True)
        days = data.groupby('day').apply(self.getEachDay)
        return days
        #return map(frozenset, C1)
    
    def process(self, data):
        #print data.head()
        """
        data 上涨或者下跌的股票数据
        return 
            rules       股票之前的协同概率
            support     每个股票组合之间的支持度
        """
        arr = self.formatData(data)
        self.__totalSupport = arr.shape[0]
        C1 = self.createSet(arr)
        #print C1
        support = self.getSupport(arr, C1)
        eleNum = 1
        eles = [support.keys()]
        #整理所有的支持度
        while (len(eles[eleNum - 1]) > 0):
            #print len(eles[eleNum - 1]), eleNum - 1
            #print eles[eleNum - 1]
            #exit()
            Ck = self.aporiGen(eles[eleNum - 1], eleNum + 1)
            print len(Ck), eleNum + 1
            #Ck = self.aporiGen(support.keys, eleNum + 1)
            supportK = self.getSupport(arr, Ck)
            support.update(supportK)
            eles.append(supportK.keys())
            eleNum += 1
            #print len(eles[eleNum - 1]), eleNum
        #计算协同 的 支持度
        rules = {}
        #print len(support)
        exit()
        for freqSeq in support.keys():
            if len(freqSeq) < 2:
                continue;
            eles = [frozenset([code]) for code in freqSeq]
            tmp = self.rulesFromSeq(freqSeq, eles, support)
            #res[arr]
            if len(tmp):
                rules[freqSeq] = tmp
        return rules, support
        
    def __init__(self):
        self.getData()
    def init(self):
        rules_r, support_r = self.process(self.__riseData)
        rules_d, support_d = self.process(self.__downData)

        self.rules_r = rules_r
        self.rules_d = rules_d
        self.support_r = support_r
        self.support_d = support_d

        mixRule =  {}
        for cb in  (set(rules_r.keys()) | set(rules_d.keys())):
            subSet = set()
            sbR = False
            sbD = False
            if rules_r.has_key(cb):
                sbR = True
                subSet |= set(rules_r[cb].keys())
            if rules_d.has_key(cb):
                sbD = True
                subSet |= set(rules_d[cb].keys())
            #print subSet
            mixRule[cb] = {}
            for sub in subSet:
                if sbR and rules_r[cb].has_key(sub) and sbD and rules_d[cb].has_key(sub):
                    above = rules_r[cb][sub][1] * support_r[sub] + rules_d[cb][sub][1] * support_d[sub]
                    under = support_d[sub] + support_r[sub]
                    conf = float(above) / float(under)
                    #print conf, rules_r[cb][sub][1],  support_r[sub],  rules_d[cb][sub][1],  support_d[sub]
                    if conf >= self.__minConf:
                        mixRule[cb][sub] = conf
                elif sbR and rules_r[cb].has_key(sub):
                    mixRule[cb][sub] = rules_r[cb][sub][1]
                elif sbD and rules_d[cb].has_key(sub):
                    mixRule[cb][sub] = rules_d[cb][sub][1]
        self.mixRule = mixRule
            #set(rules_r.keys() | ) 
    
    def getSupport(self, data, Ck):
        """
            获取频繁集项的 支持度
            data    :   数据集
            Ck      :   频繁集项
        """
        support = {}
        # 计算每个的数量
        ssCnt = {}
        #print data
        for tid in data:
            #print  len(tid)
            for can in Ck:
                if can.issubset(tid):
                    if not ssCnt.has_key(can): ssCnt[can] = 1
                    else:   ssCnt[can] += 1
        #print ssCnt
        numItems = float(len(data))

        minSupport = int(self.__totalSupport * 0.4)
        #不关心单个的支持度，而是任意两个之间的支持度
        for ss in ssCnt:
            print ssCnt[ss] , ss
            # 如果一个股票出现的次数过少，则去掉
            if ssCnt < minSupport:
                continue
            support[ss] = ssCnt[ss] / numItems
        #print support
        return support
    
    def getAboutStock(self, stock):
        for idx in self.mixRule:
            if stock not in idx: continue
            subSet = self.mixRule[idx]
            for sub in subSet:
                if stock not in sub:continue
            print idx
            print sub
            prtStr = "\t协同度 : \t%.2f\t支持度 : %.2f\r\n" % (self.mixRule[idx][sub], (self.support_r[idx] + self.support_d[idx]))
            colour.print_yellow(prtStr)
            #colour.print_yellow("hello")
    def calMostVari(self):
        #self.__dbDf.pivot_table
        #print self.__dbDf
        potDf = pd.pivot_table(self.__dbDf, index=['code'], columns=['day'], values=['percent'])
        potDf.fillna(potDf.mean())
        #print potDf.mean()
        #potDf = potDf.dropna()
        #print potDf.head()
        index = potDf.index
        codeNum = len(index)
        #print codeNum
        #print potDf.shape
        #print potDf[['SH600651']]
        colNum = potDf.shape[1]
        variMap = {}
        variMapRev = {}
        print codeNum
        print colNum
        for i in range(codeNum):
            print i
            for j in range(i+1, codeNum):
                codeA = index[i]
                if codeA == "SH600519":
                    print "yes"
                codeB = index[j]
                #variance = 0.0
                #print potDf.iloc[i]
                #print potDf.iloc[j]
                #potDf.iloc[j] - potDf.iloc[i]
                #print type(potDf.iloc[i])
                #exit()
                #variance = np.sum(potDf.iloc[j] - potDf.iloc[i])
                #print potDf.iloc[i].shape
                #print potDf.iloc[i].dtype
                variance = calVari(potDf.iloc[j].values, potDf.iloc[i].values)
                #variance = vecgVari(potDf.iloc[j].values, potDf.iloc[i].values)
                #print variance
                #resList = sum1d(potDf.iloc[j], potDf.iloc[i])
                #print resList
                #variance = np.var(potDf.iloc[j] - potDf.iloc[i])
                #variance = np.var([6, 1, 7])
                #print variance
                #for kk in range(colNum):
                #    variance += self.calVariance(potDf.iloc[i][kk], potDf.iloc[j][kk])

                if not variMap.has_key(codeA):
                    variMap[codeA] = {}
                variMap[codeA][codeB] = variance

                if not variMapRev.has_key(codeB):
                    variMapRev[codeB] = {}
                variMapRev[codeB][codeA] = variance
                #exit()
                #print potDf[[potDf.code = codeA]]
        #print index[0]
        #for idxa in index:
        if variMap.has_key('SH600519'):
            dlist = sorted(variMap['SH600519'].iteritems(), key = lambda d:d[1])
            print dlist
    def calVariance(self, a, b):
        tmp = a - b
        return tmp * tmp

#@vectorize(["float32(float32, float32)"], target="cuda")
#@vectorize(["float32(float32, float32)"], target="cuda")
#def vectorMinusArr(a , b):
#    print type(a)
#    print type(b)
#    #return a - b

#@vectorize(["float32(f8[:], f8[:])"], target="cuda")
@jit('f4(f4[:], f4[:])')
#@vectorize(["float32(f8[:], f8[:])"], target="cuda")
#@vectorize(["int32(int32, int32)"], target="cuda")
def vectorMinus(a , b):
    #print type(a)
    #print type(b)
    return 1.1

@jit('f8(f8[:], f8[:])')
def calVari(arrA, arrB):
    #print np.var(arrA - arrB)
    return np.var(arrA - arrB)

#@guvectorize(["float64(float64[:], float64[:], float64)"], '(n),()->()')
@guvectorize(["void(float64[:], float64[:],float64[:])"], '(n),(n)->()')
def vecgVari(x, y, res):
    res[0] = np.var(x - y)
    #return np.var(x - y)
    #return res

def checkNumba():
    orgData = [1.1, 9.1]
    arr = pd.Series(orgData, dtype=np.float64)
    #arr = np.Series()
    print type(np.random.random(10))
    print type(arr.values)
    print ""
    print arr
    print arr.values.shape
    print arr.values.dtype
    print ""
    print np.random.random(4)
    print np.random.random(4).shape
    print np.random.random(4).dtype
    #print type(arr)
    #B = np.ones(2, dtype=np.float32 )
    print sum1d(np.random.random(4))
    print sum1d(arr.values)

if __name__ == '__main__':
    obj = StockApori()
    obj.calMostVari()
    #checkNumba()
    print "done"
    #obj.init()
    #obj.getAboutStock("SH600258")

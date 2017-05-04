# -*- coding:utf-8 -*- 

import db
import pandas as pd
import datetime as dtime
import time

class StockApori:
    __supportData = {}

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
        startTime = dtime.datetime.strptime("20021114", "%Y%m%d") 
        #startTime = dtime.datetime.now()
        endTime  = dtime.timedelta(days=30) + startTime
        dataSql = "select percent, time, code from history where time >= '%d' and time <= '%d' limit 100" % (
            int(time.mktime(startTime.timetuple())) , int(time.mktime(endTime.timetuple())))
        #print dataSql
        dbDf = pd.read_sql(dataSql, con = db.conn)
        #print dbDf.head()
        #一天为单位 获取数据
        #dbDf = dbDf.sort_values('time', axis=0, ascending=True)
        # 标记日子
        dbDf['day'] = dbDf['time'].apply(self.markDay)
        # 获取
        self.__riseData = dbDf[dbDf.percent > 0]
        #print self.__riseData.head()
        self.__downData = dbDf[dbDf.percent < 0]
        #print self.__downData.shape

    def rulesFromSeq(self, freqSeq, Ck, support):
        m = len(Ck[0])
        res = []
        if (len(freqSeq) > m + 1):
            cand = self.aporiGen(Ck, m + 1)
            res = self.calConf(freqSeq, cand, support)
            #print res
            if len(cand) > 1:
                tmp = self.rulesFromSeq(freqSeq, cand, support)
                res.extend(tmp)
            return res
        return []


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
                L1 = list(data[i])[:length - 2]
                L2 = list(data[j])[:length - 2]
                L1.sort()
                L2.sort()
                if L1 == L2:
                    #print type(data[i])
                    retList.append(data[i] | data[j])
        return retList

    def calConf(self, freqSet, Ck, support):
        """
            获取最小支持度
        """
        result = []
        for can in Ck:
            conf = support[freqSet] / support[freqSet - can]
            if self.__minConf < conf:
                # 当freqSeq - can 出现的时候，freqSet 出现的频率
                result.append((freqSet - can, can, conf))
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
        arr = self.formatData(data)
        C1 = self.createSet(arr)
        #print C1
        support = self.getSupport(arr, C1)
        eleNum = 1
        eles = [support.keys()]
        #整理所有的支持度
        while (len(eles[eleNum - 1]) > 0):
            Ck = self.aporiGen(eles[eleNum - 1], eleNum + 1)
            #Ck = self.aporiGen(support.keys, eleNum + 1)
            supportK = self.getSupport(arr, Ck)
            support.update(supportK)
            eles.append(supportK.keys())
            eleNum += 1
        #计算协同 的 支持度
        res = {}
        print arr
        for freqSeq in support.keys():
            if len(freqSeq) < 2:
                continue;
            eles = [frozenset([code]) for code in freqSeq]
            #print "_______-"
            print freqSeq
            res = self.rulesFromSeq(freqSeq, eles, support)
            for val in res:
                print "\t\t", val[0], "\t", val[2]
            print ""
        exit()
         
        
    
    def main(self):
        self.getData()
        self.process(self.__riseData)
        self.process(self.__downData)

        

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

        #不关心单个的支持度，而是任意两个之间的支持度
        for ss in ssCnt:
            support[ss] = ssCnt[ss] / numItems
        #print support
        return support
if __name__ == '__main__':
    obj = StockApori()
    obj.main()

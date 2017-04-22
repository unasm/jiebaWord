# -*- coding:utf-8 -*-
import urllib2
import datetime
import re
import simplejson as json
#import json
from bs4 import BeautifulSoup
import MySQLdb as mysql
import time
import word
import hot
import db
import numpy as np
import getData
import strip
import pandas as pd 
import pycuda.autoinit
import pycuda.driver as drv

#from pycuda.compiler import SourceModule

class Main:
    #word对象
    __wordObj = None

    #获取指定文章的连接,标题,时间, 相关热词
    def getArtById(self, artId):
        wordSql = "select `title`, `href`, `release_time`, `id` from article where id = %s" % (artId)
        row = db.getOne(wordSql)

        print row[2], "\t", row[0]
        print "\t\t", row[1]

        #print type(self.__wordObj)
        if self.__wordObj == None:
            print "Please execute getHot first !!!"
            return
        #artWords = self.__wordObj.getArtTopN(artId)
        #显示对应的key top word 列表
        if self.__wordObj.dispAllWords(artId) == False:
            print "no words"
            return 
        #for word in artWords:
        #    print word['word'], "\t", word['count'], word["weight"], word['wordArtCnt'], word['selfFreq'], word['freqCoff']

    def getBaseTime(self):
        return self.__baseTime.strftime("%Y-%m-%d")

    #设置 基准时间,如果命令中有指定时间，则按照命令时间，否则根据基准时间给出数据，默认是今天
    def setBaseTime(self, time = ''):
        if time == '':
            self.__baseTime = datetime.datetime.now()  
        else:
            self.__baseTime = datetime.datetime.strptime(time, "%Y%m%d")
        #print self.__baseTime

    # 给定单词，列出包含这个单词的文章列表(不超过40篇)，受基准时间限制
    def getArtByWord(self, word):
        wordStr = ''
        if type(word) == type('a'):
            wordStr = word
        else:
            wordStr = "','".join(word)
        timeStart = self.__baseTime.strftime("%Y-%m-%d 00:00:00")
        timeEnd = self.__baseTime.strftime("%Y-%m-%d 23:59:59")
        wordSql = "select `title`, `href`, track_key.article_id, release_time from article inner join track_key \
                where track_key.article_id = article.id and track_key.word in('%s') and release_time >= '%s' and release_time <= '%s' \
                limit 40" % (wordStr, timeStart, timeEnd)
        #print wordSql
        dbList = db.GetList(wordSql)
        for val in dbList:
            print val[2], "\t", val[3], "\t", val[0]
            print "\t\t", val[1]
        return dbList

    def getHelp(self):
        print '''
    help: \t展示帮助信息
    getTime: \t显示当前的基准时间
    setTime: \t设置当前的基准时间
    fixData: \t重新抓取之前抓取失败的文章
    getData: \t从东方财富网抓取最新的数据
    getHot: \t显示基准时间内的热词,列1:词语 列2:pr值 列3:词语出现在的文章数
    getWordArt: \t显示指定词语对应的文章列表，
    getArt: \t指定文章id，显示文章的信息
    allWord: \t显示全部的分词结果
    getArtNum: \t当日文章数量
    getArts: \t当日文章列表
    '''
    def __init__(self):
        #return
        self.setBaseTime()
        while(1):
            command = raw_input("先生，请问您想要什么:\r\n")
            comLen = len(command)
            
            if command == "getTime":
                print "你好先生，现在的基准时间是:\t", self.getBaseTime()
            elif comLen >= 7 and command[:7] == "setTime":
                comArr = command.split()
                if len(comArr) >= 2:
                    self.setBaseTime(comArr[1])
                else: 
                    self.setBaseTime()
            elif command == "fixData":
                getData.FixArtData()
                strip.getUnParseData()
            elif command == "getData":
                #抓取数据
                getData.getDataEntry()
                #对全部的数据进行分词
                strip.getUnParseData()
            elif comLen >= 6 and command[:6] == "getHot":
                # 展示全部的 文章的分词结果
                comArr = command.split()
                dataDay = self.__baseTime
                if len(comArr) >= 2:
                    dataDay = datetime.datetime.strptime(comArr[1], "%Y%m%d")
                timeStart = dataDay.strftime("%Y-%m-%d 00:00:00")
                timeEnd = dataDay.strftime("%Y-%m-%d 23:59:59")
                if self.__wordObj == None or self.__wordObj.timeStart != timeStart:
                    self.__wordObj = word.Word(timeStart, timeEnd)
                    topKeys = self.__wordObj.getArtTopN()
                    print "process article done, ready for the hot words"
                    self.__hotObj = hot.Hot(topKeys)

                if len(comArr) >= 3:
                    self.__hotObj.dispTopPr(comArr[2])
                else:
                    self.__hotObj.dispTopPr(20)
            elif comLen >= 10 and command[:10] == "getWordArt":
                comArr = command.split()
                dataDay = self.__baseTime
                if len(comArr) < 2:
                    print "请输入类似'getWordArt 茅台 红酒'字样"
                    continue
                comArr.pop(0)
                self.getArtByWord(comArr)
                #指定包含某个单词的文章列表，显示href, title, id
            elif command == "getArtNum":
                #dataDay = self.__baseTime.strptime("20161219", "%Y%m%d")
                timeStart = self.__baseTime.strftime("%Y-%m-%d 00:00:00")
                timeEnd = self.__baseTime.strftime("%Y-%m-%d 23:59:59")
                sql = "select count(*) as cnt from article where release_time >= '%s' and release_time <= '%s'" % (timeStart, timeEnd)
                dbDf = pd.read_sql(sql, con=db.conn)
                print "共有 %d 篇文章" % dbDf['cnt'][0]
            elif command == "getArts":
                timeStart = self.__baseTime.strftime("%Y-%m-%d 00:00:00")
                timeEnd = self.__baseTime.strftime("%Y-%m-%d 23:59:59")
                sql = "select `title`, `href`, `release_time`, `id` from article where release_time >= '%s' and release_time <= '%s'" % (timeStart, timeEnd)
                rows = db.GetList(sql)
                for row in rows:
                    print row[3], "\t", row[2], "\t", row[0]
                    print "\t\t", row[1]
                    print ""
            elif comLen >= 6 and command[:6] == "getArt":
                comArr = command.split()
                if len(comArr) >= 2:
                    self.getArtById(comArr[1])
            elif command == "allWord":
                if self.__wordObj == None:
                    print "请首先分词, dispHot !!"
                self.__wordObj.dispAllWords()
            elif command == "q" or command == "exit":
            #离开
                break
            else: 
                self.getHelp()
            print ""
aa = Main()

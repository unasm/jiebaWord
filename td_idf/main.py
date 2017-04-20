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

import pycuda.autoinit
import pycuda.driver as drv

#from pycuda.compiler import SourceModule

class Main:
    __name = 'jack'
    def getName(self):
        #print "ada"
        print self.__name
    #获取指定文章的连接,标题,时间
    def getArtById(self, artId):
        wordSql = "select `title`, `href`, `release_time`, `id` from article where id = %s" % (artId)
        row = db.getOne(wordSql)
        print row[2], row[0]
        print row[1]

    #获取指定文章的topKey, 如果不在分词之中，则返回提示
    def getArtTop(self, artId):
        print "adsfa"

    def getBaseTime(self):
        print self.__baseTime.strftime("%Y-%m-%d")

    #设置 基准时间,如果命令中有指定时间，则按照命令时间，否则根据基准时间给出数据，默认是今天
    def setBaseTime(self, time = ''):
        if time == '':
            self.__baseTime = datetime.datetime.now()  
        else:
            self.__baseTime = datetime.datetime.strptime(time, "%Y%m%d")
        print self.__baseTime

    # 给定单词，列出包含这个单词的文章列表，受基准时间限制
    def getArtByWord(self, word):
        wordStr = ''
        if type(word) == type('a'):
            wordStr = word
        else:
            wordStr = "','".join(word)
        wordSql = "select `title`, `href`, track_key.article_id  from article inner join track_key \
            where track_key.article_id = article.id and track_key.word in('%s') limit 10" % (wordStr)
        #print wordStr
        dbList = db.GetList(wordSql)
        for val in dbList:
            print val[0]
        return dbList

    def getHelp(self):
        print '''
    help: \t展示帮助信息
    getData: \t从东方财富网抓取最新的数据
    dispData: \t从东方财富网抓取最新的数据, 默认是今天，如果指定日期，则展示指定日期的,格式如 20160312
    setTime: \t设置基准时间，如 20160312 后面如果没有指定时间的话，则使用该时间
    '''
    def __init__(self):
        self.setBaseTime()
        while(1):
            command = raw_input("先生，请问您想要什么:\r\n")
            comLen = len(command)
            if command == "help":
                self.getHelp()
            elif command == "getTime":
                self.getBaseTime()
            elif comLen >= 7 and command[:7] == "setTime":
                comArr = command.split()
                if len(comArr) >= 2:
                    self.setBaseTime(comArr[1])
                else: 
                    self.setBaseTime()
            elif command == "getData":
                getData.getDataEntry()
                #对全部的数据进行分词
                strip.getUnParseData()
            elif comLen >= 7 and command[:7] == "dispHot":
                comArr = command.split()

                dataDay = self.__baseTime
                if len(comArr) >= 2:
                    dataDay = datetime.datetime.strptime(comArr[1], "%Y%m%d")
                timeStart = dataDay.strftime("%Y-%m-%d 00:00:00")
                timeEnd = dataDay.strftime("%Y-%m-%d 23:59:59")

                wordObj = word.Word(timeStart, timeEnd)
                topKeys = wordObj.getArtTopN()

                #print topKeys
                aa = hot.Hot(topKeys)
                aa.dispTopPr(10)
                #print timeStart
            elif comLen >= 6 and command[:6] == "getArt":
                comArr = command.split()
                if len(comArr) >= 2:
                    self.getArtById(comArr[1])
            #获取总的热词
            #elif command == "getHot":
            elif command == "q" or command == "exit":
                #离开
                break
            print ""
aa = Main()
#aa.getName()

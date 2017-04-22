# -*- coding:utf-8 -*-
# 从网站抓取数据
import urllib2
import datetime
import re
import simplejson as json
#import json
from bs4 import BeautifulSoup
import MySQLdb as mysql
import time
import strip
import db

timeFormat = "%Y-%m-%d %H:%M:%S"
# 获取一行tr的数据
def getTrData(tr):
    arrNode = {}
    #print tr.name
    tds = tr.find_all("td")
    if len(tds) != 8:
        raise Exception("get_tdsNum_error")
    #获取时间
    span = tds[0].find_all("span")
    if len(span) != 1:
        raise Exception("show_have_one_span")
    if not span[0].has_attr("title"):
        raise Exception("span_no_title")
    # 时间
    # print span[0]["title"]
    arrNode['release_time'] = span[0]["title"]
    anode = tds[7].find_all("a")
    if len(anode) != 1:
        raise Exception("show_have_href_node")
    #print anode[0].get_text()
    #消息源
    arrNode['source'] = anode[0].get_text()
    anode = tds[4].find_all("a")
    if len(anode) != 1:
        raise Exception("shold_have_link_node")
    arrNode['title'] = anode[0]['title']
    arrNode['href'] = anode[0]['href']   
    return arrNode

# 获取一行的数据
# path 可以是url，也可以是本地的地址，
# isLocal 是否是本地的资源

def getHtmlData(path, isLocal):
    if isLocal: 
        fp = open(path)
        content = fp.read()
        fp.close()
    else: 
        content = urllib2.urlopen(path).read()
        #content = urllib2.urlopen('http://www.baidu.com').read()

    dataArr = {}
    try: 
        soup = BeautifulSoup(content, "html.parser")
        conts = soup.find_all(class_="tb14", limit=2)
        tbody = conts[0].find_all("tbody")
        if len(tbody) != 1:
            raise Exception("show have one body")
        trs = tbody[0].find_all("tr")
        #print trs[0].name
        cnt = 0
        for tr in trs:
            arrNode  = getTrData(tr)            
            dataArr[cnt] = arrNode
            cnt = cnt + 1
        #print len(dataArr)
    except Exception,ex:
        print Exception,":",ex  
    return dataArr

class User(object):
    def __init__(self, name, username):
        self.name = name
        self.username = username
def object_decoder(obj):
    print obj
    if '__type__' in obj and obj['__type__'] == 'User':
        return User(obj['name'], obj['username'])
    return obj


def jsonString(strData):
    #char[] temp = s.toCharArray();       
    s = list(strData)
    n = len(strData)
    #for i = 0; i < n; i++:
    cnt = 0
    for i in range(0, n):
        #if (s[i] == ',' or s[i] == ':' or s[i] == '[' or s[i] == '{') and s[i+1] == '"':
        if s[i] == '\\':
            s[i] = ' '

        if s[i] == '"':
            cnt = cnt + 1
            if cnt % 2 == 0:
                continue

            #for j = i + 2;j < n; j++:
            for j in range(1 + i, n):
                #s[j] = ''
                if s[j] == '"':
                    if s[j+1] != ',' and  s[j+1] != '}' and s[j+1] != ']' and s[j+1] != ':':
                        #print "asdfa", s[j+1]
                        #print "replacing"
                        s[j] = '\''
                    #elif s[j+1] == ',' or s[j+1] == '}':
                else :
                    #print "second", j
                        break 
    return ''.join(s)


#pageData = getData("http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&code=&sc=&ps=50&p=3&js=var%20jpPdmCvt={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&rt=49388255", 0)
#pageData = getData("/Users/tianyi/Desktop/python.data", 1)
#isLocal  是否从本地获取数据
def getData(path, isLocal):
    if isLocal: 
        fp = open(path)
        content = fp.read()
        fp.close()
    else: 
        content = urllib2.urlopen(path).read()
        content = content[content.find("=", 0, 20) + 1:]
        #print content
    content = jsonString(content)
    j = json.loads(content)

    # 已经充分抓取过了
    storeData = 0
    for k in range(0,len(j['data'])):
        storeData += 1
        print "idx is : ", k
        row = j['data'][k].split(",")
        dateTimer = time.strptime(row[1],'%Y/%m/%d %H:%M:%S')
        dateStr =  time.strftime("%Y%m%d", dateTimer)
        href = "http://data.eastmoney.com/report/" + dateStr + "/hy," + row[2] + ".html"
        for i in range (0, 3):
            #最多尝试三次
            try:
                content = urllib2.urlopen(href).read().decode("gbk").encode("utf-8")
                break
            except Exception,ex:
                print href , "_____" , Exception,":",ex  
                content = ''
        nodeArr = [
                "title" ,
                "href" ,
                "release_time" ,
                "update_time" ,
                "source" ,
                "source_id" ,
                "industry" ,
                "industry_id",
                "rate" ,
                "content",
                ]
        dataObj = (
                row[9], 
                href, 
                row[1],
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                row[4], 
                row[3], 
                row[10],
                row[6],
                str(int(float(row[11]) * 100)),
                content,
                )
        oldData = db.get({"href" : href},"article")
        if oldData == None:
            print href
            storeData = 0
            db.Insert(nodeArr, dataObj, "article")
        if storeData > 5:
            print "数据抓取完毕"
            return False
    return True

# 补充数据,content 为 空的
def FixArtData():
    dataArr = db.GetList("select id, href from article where content = ''")
    #href = "http://data.eastmoney.com/report/" + dateStr + "/hy," + row[2] + ".html"
    for art in dataArr:
        for i in range (0, 3):
            #最多尝试三次
            try:
                content = urllib2.urlopen(art[1]).read().decode("gbk").encode("utf-8")
                break
            except Exception,ex:
                print art[1] 
                print ex  
                content = ''
        if content == '':
            print "still empty"
            continue
        nodeArr = [
           'content',
        ]
        dataObj = (
            content,
        )
        db.update(nodeArr, dataObj, {'id' : str(art[0])}, 'article')

#获取数据的入口
def getDataEntry():
    pageSize = 50
    pageNum = (5797 / pageSize) + 1
    for i in range(0, 100):
        url = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&code=&sc=&ps=" + str(pageSize) + "&p=" + str(i) + "&js=var%20jpPdmCvt={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&rt=49388255"
        print i, "____", url
        if getData(url, 0) == False:
            break

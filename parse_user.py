# -*- coding:utf-8 -*- 

import sys


#debt_uuid
#creditor
#debtor
#origin_price
#tag

userData = {}
userTag = {}
#userData[0] = {}
#userData[0][0] = {"times":0, "amount" : 0}
#userData[0][1] = {"times":0, "amount" : 9}
#userData[0][2] = {"times":0, "amount" : 2}
#userData[0][3] = {"times":0, "amount" : 3}
#dict = sorted(userData[0].iteritems(), key = lambda d:d[1], reverse = True)
#print dict
if len(sys.argv) < 2:
    print "请输入数据文件地址"
    exit()
for line in open(sys.argv[1]):
    line = line.strip().split()
    print line
    if not userData.has_key(line[1]):
        userData[line[1]] = {}
        userTag[line[1]] = line[4]

    if not userData[line[1]].has_key(line[2]):
        userData[line[1]][line[2]] = {"times":0, "amount" : 0}
    #有N笔交易
    userData[ line[1] ][ line[2] ]['times'] += 1 
    #有N笔交易
    userData[ line[1] ][ line[2] ]['amount'] += int(line[3])
for key in userData:
    udata = userData[key] 
    print key,
    print 
    sortUData = sorted(udata.iteritems(), key = lambda d:d[1], reverse = True)
    cnt = 0
    for link in sortUData:
        print link[0]
        print link[1]['amount']
        print link[1]
        #print sortUData[1]
        cnt += 1
        if cnt > 5:
           break
    break

# -*- coding:utf-8 -*- 
import matplotlib.pyplot as plt  
import numpy as np
import sys

cnt = 0
tagAgeCnt = {}
tagAgeCnt[0] = {}
tagAgeCnt[1] = {}
if len(sys.argv) < 2:
    print "请指定路径"
    exit()
for line in open(sys.argv[1]):
    #print line
    lineArr = line.strip().split()
    if lineArr[2] == "NULL":
        #print "nulads a sdf ad a l"
        #break
        continue
    #age = float(lineArr[2])
    age = int(float(lineArr[2]))
    tag = int(lineArr[0])
    if not tagAgeCnt[tag].has_key(age):
        tagAgeCnt[tag][age] = 0
        #print "asda"

    tagAgeCnt[tag][age] += 1
    #if cnt > 10:
        #break
    cnt += 1
    #print lineArr;
width = 0.5
fig = plt.figure(1)
ax = fig.add_subplot(1, 1, 1)
#ax = fig.add_subplot(2, 1, 2)
#ax = fig.add_subplot(1, 1, 2)

freqArr = dict(sorted(tagAgeCnt[1].iteritems(), key = lambda d:d[0], reverse = False))
freqArr_0 = dict(sorted(tagAgeCnt[0].iteritems(), key = lambda d:d[0], reverse = False))

lenArr = min(len(freqArr), len(freqArr_0))
values_0 = freqArr.values()

keyArr = [i + 0.5 for i in freqArr.keys()]
ax.bar(keyArr, values_0, width, color = "green")
ax.bar(freqArr_0.keys(), freqArr_0.values(), width, color = "red")
#ax.bar(keyArr, values, width, color = "red")
ax.set_xticks(freqArr.keys())
ax.set_xlabel('items')
ax.set_ylabel('values')

    
#print
#tagList = dict(sorted(tagAgeCnt[0].iteritems(), key = lambda d:d[0], reverse = False))
#print tagList
#print type(tagList)
#showBar(tagList)
#print sorted(tagAgeCnt[1].iteritems(), key = lambda d:d[0], reverse = False)[: 10]


plt.grid(True)
plt.show()

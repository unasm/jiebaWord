# -*- coding:utf-8 -*-
import db
#import chardet
import sys

reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
#print sys.getdefaultencoding()


paths = [
        #'/Users/tianyi/project/jieba/build/lib/jieba/dict.txt',
        #'/Users/tianyi/project/jieba/jieba/dict.txt',
        '/Users/tianyi/project/jieba/proj/new_dict.txt',
        ]
nodeArr = [
        'frequency' ,
        'word',
        'flag',
        'kind'
    ]
for path in paths:
    fp = open(path, 'r')
    #result = chardet.detect(fp.read())
    while True:
        line = fp.readline()
        #print line
        arr = line.split(" ")
        if not line:
            break

        #where['word'] = arr[0]
        row = db.get({"word" : arr[0]}, 'word_attr')
        if not row :
            #print len(arr[2].strip()), arr[2].strip()
            dbObj = (arr[1] , arr[0], arr[2].strip(), '1')
            db.Insert(nodeArr, dbObj, 'word_attr')

import db
#import chardet
import sys

path = '/Users/tianyi/project/jieba/proj/new_dict.txt'
fp = open(path, 'w')
limit = 0;
sql = "SELECT * FROM stock where id > %d" % limit
print sql
stList = db.GetList(sql)
strToWrite = ""
for stock in stList:
    strToWrite = strToWrite + stock[1] + " 200 " + "nt\r\n"
    strToWrite = strToWrite + stock[2] + " 200 " + "nt\r\n"
    strToWrite = strToWrite + stock[3] + " 200 " + "nt\r\n"
#print strToWrite
fp.write(strToWrite)
fp.close()

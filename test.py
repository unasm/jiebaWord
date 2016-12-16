# -*- coding:utf-8 -*-
import urllib2
import datetime
import re
import simplejson as json
#import json
from bs4 import BeautifulSoup
import MySQLdb as mysql
import time
import db
    
rowId = 2371
oldData = db.get({"id" : str(rowId)},"article")
content = urllib2.urlopen(oldData[2]).read().decode("gbk").encode("utf-8")
db.update(['content'], (content, ), {'id' : str(rowId)}, "article")
#db.update(['content'], (content), {'id' : str(rowId)}, "article")

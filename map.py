# -*- coding:utf-8 -*- 
import json
import urllib2
import time
import random
from mpl_toolkits.basemap import Basemap


 def getLocation(cityName):
     key="3aa105f287af8365fbe2abd01ad9a67b"
    baiduGeoAPI="http://api.map.baidu.com/geocoder/v2/?address="\
            + cityName.decode('gbk').encode('utf-8') + "&output=json&ak=" + key
    jsonData = urllib2.urlopen(baiduGeoAPI).read()
    time.sleep(random.random()/1000)
    jd=json.loads(jsonData)
    if jd['result']:
        lattitude = jd['result']['location']['lat']
        longtitude = jd['result']['location']['lng']
        return [lattitude,longtitude]
    else:
        return [0,0]

print getLocation('')

# -*- coding:utf-8 -*- 

from gensim import corpora, models, similarities
import gensim
import matplotlib.pyplot as plt  
from networkx.drawing.nx_agraph import graphviz_layout
import datetime
import networkx as nx
import MySQLdb 
import db
import sys
import re
#import word
import pandas as pd 
import numpy as np

#显示某个单词在历史中的出现次数，根据日期绘图
class Plot:
    def wordHistPlot(self, word , timeStart):
        wordSqlCnt = "select sum(track_key.count) as sum, floor(date_format(article.release_time, '%Y%m%d') / 10) as date  from track_key \
        inner join article on track_key.article_id = article.id where track_key.word  in ('" + word + "') and article.release_time \
        >= '" + timeStart + "' group by date" 
        #print wordSqlCnt
        dbDf = pd.read_sql(wordSqlCnt, con=db.conn)
        print dbDf.head()
        #print dbDf['sum']
        #print dbDf['sum']
        #x_ar = np.arange(1, 5, 1)
        #y_ar = np.sin(x_ar)
        #plt.plot(x_ar, y_ar, 'g')
        plt.xlabel('frequency of date')
        plt.ylabel(word.decode('utf-8'))
        #plt.xticks(x_ar, x_label)
        plt.xticks(dbDf.index, dbDf['date'], rotation = "vertical")
        #filterList = [idx for idx in dbDf.index if idx % 5 == 0]
        plt.plot(dbDf.index, dbDf['sum'], 'g')
        #plt.xticks(dbDf['date'])
        plt.show()
if __name__ == "__main__":
    pltObj = Plot()
    pltObj.wordHistPlot('汽车', '2016-12-01');

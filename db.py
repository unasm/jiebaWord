# -*- coding:utf-8 -*- 
import MySQLdb as mysql

conn = mysql.connect('localhost', 'root', '', 'analyze');
def getOne(sql):
    #print sql
    cur = conn.cursor()
    cur.execute(sql)
    return  cur.fetchone()
    #print "Database version : %s" % data

#"SELECT VERSION"
def Insert(dataArr, dataObj, tableName):
    sql = "INSERT INTO " + tableName
    cur = conn.cursor()
    keyStr = "("
    valStr = "("
    #for key in dataArr.iteritems():
    data = []
    idx = 0
    for key in dataArr:
        keyStr = keyStr + "`" + key + '`,'
        valStr = valStr + "%s,"

    keyStr = keyStr.strip(",") + ")"
    valStr = valStr.strip(",") + ")"
    sql = sql + keyStr + " VALUES "+ valStr

    try:
        cur.execute(sql, dataObj)
        #cur.executemany(sql, dataObj)
        conn.commit()
    except Exception,ex:
        print Exception,":",ex  
        conn.rollback()
    #    conn.close()
        return 0
    #conn.close()
    return 1

def GetList(sql):
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data

def getConn():
    return conn

def get(where, tableName):
    sql = "SELECT * FROM " + tableName + " where "
    for k in where:
        if hasattr(where[k], "encode"):
            sql = sql + "`" + k +"` = '" + where[k].encode("utf-8") + "' &&"
        else:
            sql = sql + "`" + k +"` = '" + str(where[k]) + "' &&"
    sql = sql.strip("&&")
    #print sql
        #sql = sql + "`" + k +"` = '" + where[k].encode("utf-8") + "'"
        #sql = sql + "`" + k +"` = '" + mysql.escape_string(where[k]) + "'"
    return getOne(sql)


def update(dataArr, dataObj, where, tableName):
    sql = "update " + tableName + " set "
    for key in dataArr:
        sql = sql + "`" + key + "` = %s,"

    sql = sql.strip(",") 
    sql = sql + " where "
    for k in where:
        sql = sql + "`" + k +"` = '" + mysql.escape_string(where[k]) + "'"

    print sql

    cur = conn.cursor()
    try:
        cur.execute(sql, dataObj)
        #cur.executemany(sql, dataObj)
        conn.commit()
    except Exception,ex:
        print Exception,":",ex  
        conn.rollback()
    #    conn.close()
        return 0
    #conn.close()
    return 1

import MySQLdb as mysql
import db

#conn = mysql.connect('localhost', 'root', '', 'analyze');
conn = db.getConn()

#blackData = None
#def getFilters(keys):
def getBlacks():
    #keys = [1,2,3]
    #if blackData == None:
    #print "getting_data"
    cur = conn.cursor()
    #argList = '\',\''.join(keys)
    #argList = ','.join(['\'%s\''] * len(keys))
    #sql = "select * from ignore_key where `word` not in ('" + argList + "')" 
    #sql = "select * from ignore_key where `word` not is_delete = 0" 
    sql = "select * from ignore_key where `is_delete` = 0" 
    #print "select * from ignore_key where `word` not in ('" + argList + "')" 
    #print "select * from ignore_key where `word` not in %s" % str(tuple(keys))
    #cur.execute("select * from ignore_key where `word` not in %s" % argList, keys)
    cur.execute( sql )
    #cur.execute("select * from ignore_key where `word` not in ("+ argList +")" )
    #cur.execute("select * from ignore_key where `word` not in ()" % argList, keys)
    return cur.fetchall()
    #return blackData
    #print blackData

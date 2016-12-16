import  pycurl
import StringIO 
checkurl="www.test.com/abc?afgf=afd" 
b=StringIO.StringIO() 
c=pycurl.Curl() 
c.setopt(pycurl.URL, checkurl) 
c.setopt(pycurl.HTTPHEADER, ["Accept:"]) 
c.setopt(pycurl.WRITEFUNCTION, b.write) 
c.setopt(pycurl.FOLLOWLOCATION, 1) 
c.setopt(pycurl.MAXREDIRS, 5) 
c.perform() 
print b.getvalue() 
print c.getinfo(c.HTTP_CODE) 
b.close() 
c.close() 

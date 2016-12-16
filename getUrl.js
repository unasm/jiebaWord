/*************************************************************************
 * File Name :  getUrl.js
 * Author  :      unasm
 * Mail :         doujm@jiedaibao.com
 * Last_Modified: 2016-12-14 22:44:47
 ************************************************************************/


//require("/Users/tianyi/Desktop/js.aspx.html")
var rf=require("fs"); 
var data=rf.readFileSync("/Users/tianyi/Desktop/js.aspx.html","utf-8");  

//console.log(data);  
//var jsName = "jpPdmCvt";
var repData = data.replace(/\"/g,"'")
console.log(repData)
var rsData = eval(repData);
console.log(jpPdmCvt);
//eval(jpPdmCvt);
//var xgdatavt
//console.log(xgdata)
function getData(url, charset, callback) {
    var _js = document.createElement('script');
    var _this = this;
    var charset = 'utf-8';
    if (!(charset == null || charset == '')) { 
        _js.setAttribute('charset', charset); 
    }
    _js.setAttribute('type', 'text/javascript');
    _js.setAttribute('src', url);
    document.getElementsByTagName('head')[0].appendChild(_js);
    _js.onload = _js.onreadystatechange = function () {
        if (!this.readyState || this.readyState == "loaded" || this.readyState == "complete") {
            callback(_js);
            _this.removeJs(_js);
        }
    }
}

function call() {
            jsname  = "jpPdmCvt";
            console.log("jpPdmCvt")  ;
            obj = eval(jsname);
            console.log(obj);
}

var url = "http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&code=&sc=&ps=50&p=3&js=var%20jpPdmCvt={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&rt=49388255";
//getData()

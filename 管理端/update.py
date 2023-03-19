import json
import mysql.connector as mc
import requests
from bs4 import BeautifulSoup as bs
import time
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
import traceback
requests.packages.urllib3.disable_warnings()

session = requests.Session()
session.mount('http://', HTTPAdapter(max_retries=3))
session.mount('https://', HTTPAdapter(max_retries=3))


def updateBookDataIntoSql(id,title,author,introduction,type_,year,json,time,isbn,marc,publisher):
    json = str(json).replace("'",'"')
    try:
        sql = "update book set title = '{}',author = '{}',introduction='{}',type='{}',year='{}',json='{}',time='{}',isbn='{}',marc='{}',publisher='{}',updated=1 where id = {};".format(title,author,introduction,type_,year,json,time,isbn,marc,publisher,id)
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        ch.execute(sql)
        db.commit()
        db.close()
    except:
        print(traceback.format_exc())
    print(title)

def delete(id):
    sql = "delete from book where id = " + str(id)
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    ch.execute(sql)
    db.commit()
    db.close()

def getBookInfoJson(marc_no):
    url = "https://opac-lib.bistu.edu.cn/opac/item.php?marc_no={}".format(marc_no)
    req = session.get(url,verify=False,timeout=5)
    req.encoding = "utf-8"
    html = bs(req.text,"html.parser")
    dl = html.find_all("dl",class_="booklist")
    bookInfoJson = {}
    for i in dl:
        dd = i.find_all("dd")[0]
        dt = i.find_all("dt")[0]
        key = dt.text.replace(":","").replace(" ","")
        value = dd.text
        bookInfoJson[key] = value

    return bookInfoJson

def getBookCover(isbn):
    url = "https://opac-lib.bistu.edu.cn/opac/ajax_isbn_marc_no.php?isbn={}".format(isbn)
    req = session.get(url,verify=False,timeout=5)
    resultJson = json.loads(req.text)
    if resultJson.get("image") in ["",None]:
        return None
    else:
        return resultJson.get("image")

def getBookIntro(bookInfoJson):
    for i in bookInfoJson.keys():
        if "提要" in i or "文摘" in i:
            return bookInfoJson.get(i)
    return ""

def getBookType(bookInfoJson):
    type = bookInfoJson.get("学科主题")
    if type == None:
        return "其他"
    return type

def getBookInfoJson(marc_no):
    url = "https://opac-lib.bistu.edu.cn/opac/item.php?marc_no={}".format(marc_no)
    req = session.get(url,verify=False,timeout=5)
    req.encoding = "utf-8"
    html = bs(req.text,"html.parser")
    dl = html.find_all("dl",class_="booklist")
    bookInfoJson = {}
    for i in dl:
        dd = i.find_all("dd")[0]
        dt = i.find_all("dt")[0]
        key = dt.text.replace(":","").replace(" ","")
        value = dd.text
        bookInfoJson[key] = value

    return bookInfoJson

def getBookTitleJson(title):
    url = "https://opac-lib.bistu.edu.cn/opac/ajax_search_adv.php"
    data = {
        "searchWords": [{
            "fieldList": [{
                "fieldCode": "",
                "fieldValue": title
            }]
        }],
        "filters": [],
        "limiter": [],
        "sortField": "relevance",
        "sortType": "desc",
        "pageSize": 20,
        "pageCount": 1,
        "locale": "",
        "first": True
    }
    req = session.post(url,json = data,verify=False,timeout=5)
    req.encoding = "utf-8"
    resultJson = json.loads(req.text)
    return resultJson["content"][0]
    

if __name__ == "__main__":
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select id,title from book where updated = 0"
    ch.execute(sql)
    result = ch.fetchall();
    total = len(result)
    count = 0
    db.close()
    with ThreadPoolExecutor(10) as t:
        for i in result:
            try:
                id = i[0]
                title = i[1]
                lineJson = getBookTitleJson(title)
                author = lineJson.get("author")
                isbn = lineJson.get("isbn")
                marc = lineJson.get("marcRecNo")
                year = lineJson.get("pubYear")
                title = lineJson.get("title")

                infoJson = getBookInfoJson(marc)

                introduction = getBookIntro(infoJson).replace("'",'"')
                publisher = lineJson.get("publisher")
                updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                
                type = getBookType(infoJson)

                t.submit(updateBookDataIntoSql,id,title,author,introduction,type,year,infoJson,updateTime,isbn,marc,publisher)
                count += 1
                print("{} / {}".format(count,total))
                # updateBookDataIntoSql(id,title,author,introduction,type,year,infoJson,updateTime,isbn,marc,publisher)
            except:
                delete(i[0])
                print(i)
            


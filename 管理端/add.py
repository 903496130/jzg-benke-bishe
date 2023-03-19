import json
import time
from concurrent.futures import ThreadPoolExecutor
import mysql.connector as mc

import requests
from bs4 import BeautifulSoup as bs

import dao
import traceback



requests.packages.urllib3.disable_warnings()

def getBookInfoJson(marc_no):
    url = "https://opac-lib.bistu.edu.cn/opac/item.php?marc_no={}".format(marc_no)
    req = requests.get(url,verify=False)
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
    req = requests.get(url,verify=False)
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

def readTxtByLine():



    with ThreadPoolExecutor(10) as t:
        while True:

            line = f.readline().replace("\n","").replace("'",'"')
            try:
                if line:
                    lineJson = json.loads(line)
                    author = lineJson.get("author")
                    isbn = lineJson.get("isbn")
                    marc = lineJson.get("marcRecNo")
                    year = lineJson.get("pubYear")
                    title = lineJson.get("title")
                    if dao.isBookExists(title):
                        continue
                    
                    infoJson = getBookInfoJson(marc)
                    cover = getBookCover(isbn)
                    # if cover == None or "nobook" in cover or 


                    introduction = getBookIntro(infoJson).replace("'",'"')
                    publisher = lineJson.get("publisher")
                    updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                    
                    type = getBookType(infoJson)
                    id = dao.getId()

                    t.submit(dao.saveBookDataIntoSql,id,title,author,introduction,type,year,infoJson,updateTime,cover,isbn,marc,publisher)
                    # dao.saveBookDataIntoSql(id,title,author,introduction,type,year,infoJson,updateTime,cover,isbn,marc,publisher)
                else:
                    break
            except:
                print(traceback.format_exc())

if __name__ == "__main__":
    # db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    # ch = db.cursor()
    # sql = "select id,json from "
    # lst = 

    getBookType(getBookInfoJson("52314c486c69455143367863573561562b56474638413d3d"))





import requests
import json
import time
from bs4 import BeautifulSoup as bs

requests.packages.urllib3.disable_warnings()

def saveInfoIntoTxt(content):
    with open("save.txt","a",encoding="utf-8") as f:
        f.write(str(content) + "\n")

def getBookInfoBySearch(pageNum):
    header = {'content-type': "application/json"}
    body = {
        "searchWords": [{
            "fieldList": [{
                "fieldCode": "",
                "fieldValue": "著"
            }]
        }],
        "filters": [],
        "limiter": [],
        "sortField": "relevance",
        "sortType": "desc",
        "pageSize": 20,
        "pageCount": pageNum,
        "locale": "zh_CN",
        "first": True
    }
    url = "https://opac-lib.bistu.edu.cn/opac/ajax_search_adv.php"
    req = requests.post(url, headers=header,json=body,verify=False)
    resultJson = json.loads(req.text)
    for i in resultJson["content"]:
        saveInfoIntoTxt(i)

def getBookCover(isbn):
    url = "https://opac-lib.bistu.edu.cn/opac/ajax_isbn_marc_no.php?isbn={}".format(isbn)
    req = requests.get(url)
    resultJson = json.loads(req.text)

def savePageNum(pageNum):
    with open("page.txt","w",encoding="utf-8") as f:
        f.write(str(pageNum) + "\n")

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


if __name__ == "__main__":
    # getBookDetail("457a45506b53553578793268694d44626b41754f31513d3d")
    getBookInfoBySearch(1)



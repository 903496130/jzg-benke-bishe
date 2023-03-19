import re
import mysql.connector as mc
import random
import traceback
import json
import math
import time

def getId():
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    id = random.randint(1000000,99999999)
    ch.execute("select * from book where id = {}".format(id))
    if ch.fetchone() != None:
        db.close()
        return getId()
    else:
        db.close()
        return id

def isBookExists(title):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    id = random.randint(1000000,99999999)
    ch.execute("select * from book where title = '{}'".format(title))
    if ch.fetchone() != None:
        db.close()
        return True
    else:
        db.close()
        return False

def saveStoreInfo(bid,storePlace,num):

    sql = "insert into store (bid,putPlace,total) values ({},'{}',{})".format(bid,storePlace,num)
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    ch.execute(sql)
    db.commit()
    db.close()

def getStoreInfo(bid):
    data = {}
    sql = "select putPlace,total from store where bid = {}".format(bid)
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    ch.execute(sql)
    result = ch.fetchall()
    for i in result:
        data[str(i[0])] = str(i[1])
    db.close()
    return data

def deleteBook(bid):
    try:
    
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "delete from book where id = {}".format(bid)
        ch.execute(sql)
        db.commit()
        db.close()
        deleteStore(bid)
        return json.dumps({"msg":"删除成功"})
    except:
        return json.dumps({"msg":"删除失败"})

def addGG(title,content):
    try:
        content = content.replace(" ","&nbsp;").replace("\n","<br>").replace("'","")
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = "insert into gg (id,title,content,date) values ({},'{}','{}','{}')".format(getId(),title,content,now)
        ch.execute(sql)
        db.commit()
        db.close()
        return {"msg":"添加公告成功"}
    except:
        return {"msg":"添加公告失败"}

def removeGG(id):
    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "delete from gg where id = {}".format(id)
        ch.execute(sql)
        db.commit()
        db.close()
        return {"msg":"删除成功"}
    except:
        return {"msg":"删除失败"}

def deleteStore(bid):

    try:
        db1 = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch1 = db1.cursor()
        sql = "delete from store where bid = {}".format(bid)
        ch1.execute(sql)
        db1.commit()
        db1.close()
        return json.dumps({"msg":"删除成功"})
    except:
        return json.dumps({"msg":"删除失败"})

def removeJy(uid,bid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "delete from jy where bid = {} and uid = {}".format(bid,uid)
    ch.execute(sql)
    db.commit()
    db.close()


def personInfoChange(username,nickname,head,sign):
    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "update user set nickname = '{}',head = '{}',sign='{}' where username = {}".format(nickname,head,sign,username)
        ch.execute(sql)
        db.commit()
        db.close()
        return {"msg":"修改成功"}
    except:
        return {"msg":"修改失败"}

def saveBookDataIntoSql(id,title,author,introduction,type_,year,json,time,cover,isbn,marc,publisher):
    json = str(json).replace("'",'"')
    if isBookExists(title):
        return
    try:
        sql = "insert into book (id,title,author,introduction,type,year,json,time,cover,isbn,marc,publisher) values ({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(id,title,author,introduction,type_,year,json,time,cover,isbn,marc,publisher)
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        ch.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        print(traceback.format_exc())
        return False
    print(title)

def getOneBookListByRandom(length):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select title,author,introduction,cover,type,id,publisher,year from book order by rand() limit {}".format(length)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    resultJson = {"data":[],"length":length,"way":"random"}
    for i in result:
        id = i[5]
        title = i[0]
        author = i[1]
        introduction = i[2]
        cover = i[3]
        type = i[4]
        publisher = i[6]
        year = i[7]
        resultJson["data"].append({"year":year,"publisher":publisher,"title":title,"id":id,"author":author,"introduction":introduction,"cover":cover,"type":type})
    return resultJson

def getCommentList(keyword,page,num):
    resultJson = []
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    if keyword == None or keyword == "":
        sql = "select  SQL_CALC_FOUND_ROWS bid,uid,pid,content,time from comment order by time desc limit {},{}".format((page - 1) * num,num)
    else:
        sql = "select  SQL_CALC_FOUND_ROWS bid,uid,pid,content,time from comment where content like '%{}%' order by time desc limit {},{}".format(keyword,(page - 1) * num,num)
    ch.execute(sql)
    result = ch.fetchall()
    
    for i in result:
        bid,uid,pid,content,time = i
        title = getBookInfoById(bid)["data"]["title"]
        nickname = getUserInfoById(uid)[0]

        resultJson.append({
            "bid":bid,
            "uid":uid,
            "pid":pid,
            "content":content,
            "time":time,
            "title":title,
            "nickname":nickname
        })
    sql = "SELECT found_rows()"
    ch.execute(sql)
    total = ch.fetchone()[0]
    db.close()
    return json.dumps({"data":resultJson,"total":total})

def removeComment(uid,bid,pid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "delete from comment where uid = {} and bid = {} and pid = {}".format(uid,bid,pid)
    ch.execute(sql)
    db.commit()
    db.close()
    return json.dumps({})

def getGG():
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select title,content,date,id from gg order by date desc"
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    resultJson = {"data":[],"length":len(result)}
    for i in result:
        title = i[0]
        content = i[1]
        date = i[2]
        id = i[3]
        resultJson["data"].append({"title":title,"content":content,"date":date,"id":id})
    return resultJson

def getBookCommentById(id,page):
    numPerPage = 30
    resultJson = {}

    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select uid,pid,content,time,zan from comment where bid = {} limit {},{};".format(id,(int(page) - 1) * numPerPage,numPerPage)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    resultJson = {"data":[],"length":len(result),"code":"0"}
    for i in result:
        uid = i[0]
        pid = i[1]
        content = i[2]
        date = i[3]
        fnumber = getCommentFollowNumberById(id,pid)
        zan = i[4]
        nickname,sign,head = getUserInfoById(uid)
        resultJson["data"].append({"uid":uid,"pid":pid,"content":content,"date":date,"fnumber":fnumber,"zan":zan,
            "nickname":nickname,
            "sign":sign,
            "head":head
        })
    resultJson["code"] = "1"
    return json.dumps(resultJson)

def getCommentFollowNumberById(bid,pid):
  
    resultJson = {}

    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select uid,pid,content,time from comment where bid = {} and fid = {};".format(bid,pid)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    return len(result)


def jyDate(date):

    try:
        resultJson = []
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "select uid,bid,storeName,startDate,endDate,borrowDate,backDate,status from jy where startDate = '{}'".format(date)
        ch.execute(sql)
        result = ch.fetchall()
        for i in result:
            uid,bid,storeName,startDate,endDate,borrowDate,backDate,status = i
            nickname,sign,head = getUserInfoById(uid)
            bookname = getBookInfoById(bid)["data"]["title"]
            resultJson.append({
                "uid":uid,
                "nickname":nickname,
                "bid":bid,
                "bookname":bookname,
                "storeName":storeName,
                "startDate":str(startDate),
                "endDate":str(endDate),
                "status":status,
                "borrowDate":str(borrowDate),
                "backDate":str(backDate)
            })

        count = 1
        db.close()
        return {"data":resultJson,"total":count}
    except:
        return {"data":[],"total":1}

def checkShoucang(bid,uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select * from sc where uid = {} and bid = {}".format(uid,bid)
    ch.execute(sql)
    result = ch.fetchone()
    db.close()
    return result == None

def shoucang(bid,uid):
    now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    if checkShoucang(bid,uid):
        sql = "insert into sc (uid,bid,date) values ({},{},{});".format(uid,bid,now)
        ch.execute(sql)
        db.commit()
        return json.dumps({"code":"1","msg":"收藏成功"})
    else:
        return json.dumps({"code":"0","msg":"收藏失败，你已经收藏过这本书了"})


def getBookPfById(id):
    resultJson = {}
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select number from pf where bid = {};".format(id)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    resultJson = {"code":"0","msg":""}
    pf = 0
    if len(result) == 0:
 
        return "0","暂无评分"

    for i in result:
        pf += i[0]


    return pf/len(result),"{}人参与".format(len(result))
 

def addCommentToBook(bid,uid,fid,content):
    if fid == "" or fid == None:
        fid = 0
    
    now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "insert into comment (bid,uid,pid,fid,content,time,zan) values ({},{},{},{},'{}','{}',{});".format(bid,uid,getId(),fid,content,now,0)
        ch.execute(sql)
        db.commit()
        db.close
        return json.dumps({"code":"1","msg":"成功"})
    except:
        print(traceback.format_exc())
        return json.dumps({"code":"0","msg":"失败"})
    pass

def addPfToBook(bid,uid,score):
    if score not in [1,2,3,4,5]:
        return json.dumps({"code":"0","msg":"参数异常"})

    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    if checkPfRight(bid,uid):
        sql = "insert into pf (uid,bid,number) values ({},{},{});".format(uid,bid,score)
        ch.execute(sql)
        db.commit()
        return json.dumps({"code":"1","msg":"打分成功"})
    else:
        return json.dumps({"code":"0","msg":"打分失败，你已经打过分了"})

def checkPfRight(bid,uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select * from pf where uid = {} and bid = {}".format(uid,bid)
    ch.execute(sql)
    result = ch.fetchone()
    db.close()
    return result == None

def getBookInfoById(id):
    
    if id == None:
        resultJson = {"code":"0","msg":"你要查看的书籍不存在"}

    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select title,author,introduction,type,year,json,time,cover,isbn,marc,publisher from book where id = '{}'".format(id)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    resultJson = {"data":{},"code":"1"}

    if len(result) == 0:
        resultJson = {"code":"0","msg":"你要查看的书籍不存在"}
        return resultJson
    resultJson["data"]["id"] = id
    resultJson["data"]["title"] = result[0][0]
    resultJson["data"]["author"] = result[0][1]
    resultJson["data"]["introduction"] = "&nbsp;&nbsp;" + result[0][2].replace("。","。<br><br>&nbsp;&nbsp;")[:-20]
    resultJson["data"]["type"] = result[0][3]
    resultJson["data"]["year"] = result[0][4]
    resultJson["data"]["json"] = result[0][5]
    resultJson["data"]["time"] = result[0][6]
    resultJson["data"]["cover"] = result[0][7]
    resultJson["data"]["isbn"] = result[0][8]
    resultJson["data"]["marc"] = result[0][9]
    resultJson["data"]["publisher"] = result[0][10]
    resultJson["data"]["pf"],resultJson["data"]["pfmsg"] = getBookPfById(id)

    return resultJson

def getCommentTj():
    resultJson = {"msg":"","code":"","data":[]}
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select bid,uid,content,time,zan from comment order by rand() limit 20;"
    ch.execute(sql)
    result = ch.fetchall()
    for i in result:
        bid = i[0]
        uid = i[1]
        content = i[2]
        time = i[3]
        zan = i[4]

        nickname,sign,head = getUserInfoById(uid)

        resultJson["data"].append(
            {
                "nickname":nickname,
                "sign":sign,
                "head":head,
                "date":time,
                "bid":bid,
                "content":content,
                "zan":zan,
                "title":getBookInfoById(bid)["data"]["title"]
            }
        )
    return json.dumps(resultJson)

def getPersonalComment(uid):
    resultJson = {"msg":"","code":"","data":[]}
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select bid,uid,pid,content,time from comment where uid = {}".format(uid)
    ch.execute(sql)
    result = ch.fetchall()
    for i in result:
        bid,uid,pid,content,time = i

        nickname,sign,head = getUserInfoById(uid)
        resultJson["data"].append(
            {
                "nickname":nickname,
                "sign":sign,
                "head":head,
                "date":time,
                "bid":bid,
                "content":content,
                "pid":pid,
                "title":getBookInfoById(bid)["data"]["title"]
            }
        )
    return json.dumps(resultJson)


def scCheck(bid,uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select * from sc where uid = {} and bid = {};".format(uid,bid)
    ch.execute(sql)
    result = ch.fetchone()
    db.close()
    return result == None

def scAdd(bid,uid):
    resultJson = {"msg":"","code":"","data":[]}
    if scCheck(bid,uid):
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        sql = "insert into sc (uid,bid,date) values ({},{},'{}');".format(uid,bid,now)
        ch.execute(sql)
        db.commit()
        db.close()
        resultJson["msg"] = "收藏成功"
        resultJson["code"] = "1"
        return json.dumps(resultJson)
    else:
        resultJson["msg"] = "你已经收藏过这本书了"
        return json.dumps(resultJson)
    
def scRemove(bid,uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "delete from sc where uid = {} and bid = {};".format(uid,bid)
    ch.execute(sql)
    db.commit()
    db.close()
    return json.dumps({"msg":"取消成功"})

def scList(uid):
    resultJson = {"msg":"","code":"","data":[]}
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select bid from sc where uid = {};".format(uid)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    for i in result:
        bid = i[0]
        resultJson["data"].append(getBookInfoById(bid)["data"])
    resultJson["msg"] = "成功"
    resultJson["code"] = "1"

    if len(result) == 0:
        resultJson["msg"] = "你还没有收藏的内容"

    return json.dumps(resultJson)


def search(keywords,page,num):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select SQL_CALC_FOUND_ROWS id,title,cover from book where json like '%{}%' limit {},{}".format(keywords,(page - 1) * num,num)
    ch.execute(sql)
    result = ch.fetchall()

    dataJson = []
    resultJson = []

    for i in result:
        id = i[0]
        title = i[1]
        cover = i[2]
        dataJson.append({"id":id,"title":title,"cover":cover})
    
    sql = "SELECT found_rows()"
    ch.execute(sql)
    result = ch.fetchall()
    total = result[0][0]

    resultJson = {"code":0,"data":dataJson,"total":total,"msg":"共为您搜索到{}条结果".format(total)}

    return json.dumps(resultJson)


#==============================================================================

def reg(username,password,nickname,sign):
    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "insert into user (username,password,nickname,sign) values ({},'{}','{}','{}');".format(username,password,nickname,sign)
        ch.execute(sql)
        db.commit()
        db.close
        return json.dumps({"code":"1","msg":"注册成功"})
    except:
        return json.dumps({"code":"0","msg":"注册失败，输入错误或用户名已经存在"})

def login(username,password):

    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "select username,nickname,sign,head from user where username = {} and password = '{}'".format(username,password)
        ch.execute(sql)
        i = ch.fetchone()
        uid = i[0]
        nickname = i[1]
        sign = i[2]
        head = i[3]
        db.close()

        return json.dumps({"code":"1","nickname":nickname,"sign":sign,"uid":uid,"msg":"欢迎你," + nickname,"head":head})
        
    except:
        return json.dumps({"code":"0","msg":"登录失败！请检查用户名和密码是否正确。"})
    
def getUserInfoById(uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select username,nickname,sign,head from user where username = {}".format(uid)
    ch.execute(sql)
    i = ch.fetchone()
    nickname = i[1]
    sign = i[2]
    head = i[3]
    db.close()
    return nickname,sign,head

def jyAdd(uid,bid,storeName,startDate,endDate):
    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "insert into jy (uid,bid,storeName,startDate,endDate,status) values ({},{},'{}','{}','{}','{}')".format(
            uid,bid,storeName,startDate,endDate,"等待用户取书"
        )
        ch.execute(sql)
        db.commit()
        db.close()
        return json.dumps({"code":0,"msg":"添加借阅记录成功，请即时到图书馆取书"})
    except:
        return json.dumps({"code":100,"msg":"您已经借阅过这本书了，请勿重复借阅"})

def jyTotal(uid,page,num):
    resultJson = []
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    if uid == "" or uid == None:
        sql = "select SQL_CALC_FOUND_ROWS uid,bid,storeName,startDate,endDate,borrowDate,backDate,status from jy order by startDate desc limit {},{}".format((page-1)*num,num)
    else:
        sql = "select SQL_CALC_FOUND_ROWS uid,bid,storeName,startDate,endDate,borrowDate,backDate,status from jy where uid = {} order by startDate desc limit {},{}".format(uid,(page-1)*num,num)

    ch.execute(sql)
    result = ch.fetchall()
    
    for i in result:
        uid,bid,storeName,startDate,endDate,borrowDate,backDate,status = i
        nickname,sign,head = getUserInfoById(uid)
        bookname = getBookInfoById(bid)["data"]["title"]
        resultJson.append({
            "uid":uid,
            "nickname":nickname,
            "bid":bid,
            "bookname":bookname,
            "storeName":storeName,
            "startDate":str(startDate),
            "endDate":str(endDate),
            "status":status,
            "borrowDate":str(borrowDate),
            "backDate":str(backDate)
        })

    sql = "SELECT found_rows()"
    ch.execute(sql)
    count = ch.fetchone()[0]
    db.close()

    return {"data":resultJson,"total":count}

def jyCheck(uid,bid,status):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select status from jy where uid = {} and bid = {}".format(uid,bid)
    ch.execute(sql)
    status = ch.fetchone()[0]
    db.commit()
    db.close()
    return json.dumps({"status":status})

def jyOut():
    resultJson = []
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    sql = "select uid,bid,storeName,startDate,endDate,borrowDate,backDate,status from jy where endDate < '{}' or backDate < '{}' and status not like '%{}%'".format(now,now,"已归还")
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    for i in result:
        uid,bid,storeName,startDate,endDate,borrowDate,backDate,status = i
        nickname,sign,head = getUserInfoById(uid)
        bookname = getBookInfoById(bid)["data"]["title"]
        resultJson.append({
            "uid":uid,
            "nickname":nickname,
            "bid":bid,
            "bookname":bookname,
            "storeName":storeName,
            "startDate":str(startDate),
            "endDate":str(endDate),
            "status":status,
            "borrowDate":str(borrowDate),
            "backDate":str(backDate)
        })
    return resultJson

def jyNotback():
    resultJson = []
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    sql = "select uid,bid,storeName,startDate,endDate,borrowDate,backDate,status from jy where isNull(backDate)"

    ch.execute(sql)
    result = ch.fetchall()
    
    for i in result:
        uid,bid,storeName,startDate,endDate,borrowDate,backDate,status = i
        nickname,sign,head = getUserInfoById(uid)
        bookname = getBookInfoById(bid)["data"]["title"]
        resultJson.append({
            "uid":uid,
            "nickname":nickname,
            "bid":bid,
            "bookname":bookname,
            "storeName":storeName,
            "startDate":str(startDate),
            "endDate":str(endDate),
            "status":status,
            "borrowDate":str(borrowDate),
            "backDate":str(backDate)
        })

    return resultJson

def jyChange(uid,bid,status):
    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "select * from jy where uid = {} and bid = {}".format(uid,bid)
        ch.execute(sql)
        if ch.fetchall() == []:
            db.close()
            return json.dumps({"code":100,"msg":"查询不到借阅记录"})

        now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if "已归还" in status:
            sql = "update jy set status = '{}' , backDate = '{}' where uid = {} and bid = {}".format(status,now,uid,bid)
        elif "等待归还" in status:
            sql = "update jy set status = '{}' , borrowDate = '{}' where uid = {} and bid = {} ".format(status,now,uid,bid)
        else:
            sql = "update jy set status = '{}' where uid = {} and bid = {}".format(status,uid,bid)
        ch.execute(sql)
        db.commit()
        db.close()
        return json.dumps({"code":0,"msg":"成功更改借阅状态为" + status})
    except:
        return json.dumps({"code":100,"msg":"系统错误"})

def jyList(uid):

    resultJson = {}
    dataJson = []

    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "select bid,startDate,endDate,status from jy where uid = {}".format(uid)
        ch.execute(sql)
        data = ch.fetchall()
        db.close()
        if len(data) == 0:
            return json.dumps({"code":1,"msg":"没有数据"})
        for i in data:
            bid = i[0]
            startDate = i[1]
            endDate = i[2]
            status = i[3]
            bookInfo = getBookInfoById(bid)["data"]
            bookInfo["startDate"] = str(startDate)
            bookInfo["endDate"] = str(endDate)
            bookInfo["status"] = status
            dataJson.append(bookInfo)
        return json.dumps({"code":0,"msg":"成功","data":dataJson})
    except:
        return json.dumps({"code":100,"msg":"系统错误"})

if __name__ == "__main__":
    print(jyDate("2021-05-210"))

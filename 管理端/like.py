import mysql.connector as mc
import json
import dao


def getNum(uid,bid):
    try:
        db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
        ch = db.cursor()
        sql = "select num from behavior where uid = {} and bid = {}".format(uid,bid)
        ch.execute(sql)
        result = ch.fetchone()[0]
        db.close()
        return result
    except:
        return 0

def getBookType(bid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select type from book where id = {}".format(bid)
    ch.execute(sql)
    result = ch.fetchone()[0]
    db.close()
    return result.split("-")

def getLikeTypes(uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select bid from behavior where uid = '{}' order  by num desc limit 5".format(uid)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    total = []
    for i in result:
        bid = i[0]
        total += getBookType(bid)
    return total

def getRandomBookListByTypes(typeList):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select id from book"

    if(len(typeList) != 0):
        sql += " where "

    for i in range(len(typeList)):
        sql += " type like '%{}%' ".format(typeList[i])
        if i != len(typeList) - 1:
            sql += "or"

    sql += " order by rand() limit 30"
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    bidList = []
    for i in result:
        bidList.append(i[0])
    return bidList

def getSimilarBook(uid):
    data = []
    bidList = getRandomBookListByTypes(getLikeTypes(uid))
    for i in bidList:
        data.append(dao.getBookInfoById(i)["data"])
    return data

if __name__ == "__main__":
    print(getSimilarBook('123'))


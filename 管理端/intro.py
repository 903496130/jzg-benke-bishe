import mysql.connector as mc
import random
import traceback
import json
import math
import time

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

def addNum(uid,bid,score):
    historyScore = getNum(uid,bid)
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    score += historyScore
    if historyScore == 0:
        sql = "insert into behavior (uid,bid,num) values ({},{},{})".format(uid,bid,score)
    else:
        sql = "update behavior set num = {} where uid = {} and bid = {}".format(score,uid,bid)
    ch.execute(sql)
    db.commit()
    db.close()

def addBehavior(uid,bid,score):
    addNum(uid,bid,score)


if __name__ == "__main__":
    addBehavior(123,456,10)
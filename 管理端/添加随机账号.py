from intro import getNum
import mysql.connector as mc
import json
import dao
import random
import intro

def getBookIdRandom():
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select id from book order by rand() limit 1"
    ch.execute(sql)
    result = ch.fetchone()[0]
    db.close()
    return result

def addUser():
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    head = "http://39.106.51.168:8080/static/img/robot.jpg"
    username = random.randint(10,10000)
    nickname = "测试{}号".format(username)
    sql = "insert into user (username,password,nickname,sign,head) values ({},'{}','{}','{}','{}')".format(username,username,nickname,nickname,head)
    ch.execute(sql)
    db.commit()
    db.close()
    return username


def addBehavior():
    username = addUser()
    num = random.randint(3,12)
    for i in range(num):
        bid = getBookIdRandom()
        score = random.randint(0,10)
        intro.addBehavior(username,bid,score)
        print(i)

if __name__ == "__main__":

    for i in range(30):
        print(str(i) + "========")
        addBehavior()
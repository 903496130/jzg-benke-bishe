from intro import getNum
import mysql.connector as mc
import json
import dao
import intro
import dao

def pc(object1, object2):
    values = range(len(object1))
    
    sum_object1 = sum([float(object1[i]) for i in values]) 
    sum_object2 = sum([float(object2[i]) for i in values])

    square_sum1 = sum([pow(object1[i],2) for i in values])
    square_sum2 = sum([pow(object2[i],2) for i in values])
    product = sum([object1[i]*object2[i] for i in values])
    numerator = product - (sum_object1*sum_object2/len(object1))
    denominator = ((square_sum1 - pow(sum_object1,2)/len(object1)) * (square_sum2 - 
    	pow(sum_object2,2)/len(object1))) ** 0.5
        
    if denominator == 0:
        return 0

    result = numerator/denominator
    return result

def getUserList():
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select uid from behavior group by uid"
    ch.execute(sql)
    result = ch.fetchall()
    db.close()
    data = []
    for i in result:
        data.append(i[0])
    return data

def getBidDic(uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select bid,num from behavior where uid = {}".format(uid)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()  
    data = {}
    for i in result:
        data[i[0]] = i[1]
    return data

def getBidList(uid):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    sql = "select bid,num from behavior where uid = {}".format(uid)
    ch.execute(sql)
    result = ch.fetchall()
    db.close()  
    data = {}
    for i in result:
        data[i[0]] = i[1]
    return data


def getAverList(list):
    isZero = 0
    total = 0
    notZero = 0
    avr = 0
    for i in list:
        if i == 0:
            isZero += 1
        else:
            notZero += 1
            total += i
    avr = total / notZero

    for i in range(len(list)):
        if list[i] == 0:
            list[i] = avr
    return list

def getAver(list):
    total = 0
    for i in list:
        total += i
    return total / len(list)

def calcCorrelation(uid):

    result = {}
    lst = getUserList()
    dct = {}
    myDct = {}
    try:
        lst.remove(uid)
    except:
        pass
    
    for i in lst:
        dct[i] = getBidDic(i)
    myDct[uid] = getBidDic(uid)
    myKeys = list(myDct[uid].keys())

    for i in dct:
        totalkeys = myKeys + list(dct[i].keys())
        myScore = []
        himScore = []
        for m in totalkeys:
            myScore.append(myDct[uid].get(m) or 0)
            himScore.append(dct[i].get(m) or 0)
        myScore = getAverList(myScore)
        himScore = getAverList(himScore)
        result[i] = pc(myScore,himScore)
    return result

def getSimilarUserBookList(uid):
    result = calcCorrelation(int(uid))
    a = sorted(result.items(), key=lambda x: x[1], reverse=True)
    a = a[:1]
    lst = []
    user = []
    for i in a:
        uid = i[0]
        user.append(uid)
        lst += getBidList(uid)
    lst = tuple(lst)
    data = []
    for i in lst:
        try:
            info = dao.getBookInfoById(i)
            data.append(info["data"])
        except:
            pass
    userData = []
    for i in user:
        nickname,sign,head = dao.getUserInfoById(i)
        userData.append({"nickname":nickname,"sign":sign,"head":head})
    return {"data":data,"total":len(lst),"user":userData}

if __name__ == "__main__":
    data = getSimilarUserBookList(123)
    bookList = data["data"]
    userList = data["user"]
    
    for i in bookList:
        title = i["id"]
        print(title)
    for i in userList:
        print(i)


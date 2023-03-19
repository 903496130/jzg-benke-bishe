import web
import dao
import json
import traceback
import os
import time
import qrcode
import intro
import like
import user

urls = (

    '/',"index",

    '/system/gg',"gg",
    '/gg/add',"ggAdd",
    '/gg/remove',"removeAdd",

    '/book/info',"bookinfo",
    "/book/addpl","addComment",
    '/book/getpl',"getComment",
    '/book/pingfen',"pingfen",
    '/book/delete',"delete",
    '/book/store',"bookStore",

    '/book/borrow',"bookBorrow",
    '/book/back',"bookBack",


    '/jy/add','jyAdd',
    '/jy/change','jyChange',
    '/jy/list','jyList',
    '/jy/cancel','jyCancel',
    '/jy/check','jyCheck',

    '/jy/notback','jyNotback',
    '/jy/out','jyOut',
    '/jy/date','jyDate',

    '/jy/total','jyTotal',

    '/sc/add','scAdd',
    '/sc/remove','scRemove',
    '/sc/list','scList',

    "/comment/tj","cTuijian",
    "/comment/gr","cGeRen",
    "/comment/list","cList",
    "/comment/remove","cRemove",

    '/user/intro', 'randomList',
    '/user/login', 'login',
    '/user/reg','reg',
    '/user/info/change',"userInfoChange",

    '/book/search','search',

    '/tj/user','tjUser',
    '/tj/book','tjBook',

    "/bookAdd","bookAdds",
    "/bookManage","bookManage",
    "/bookSearch","bookSearch",
    "/borrowManage","borrowManage",
    "/commentManage","commentManage",
    "/face","face",
    "/ggManage","ggManage",
    "/login","loginPage",
    "/userInfoManage","userInfoManage",
    "/details","details",
    "/update","update"

)

dct = {
    "sc":5,
    "pl":2,
    "jy":10
}

admin = {"admin123":"123"}

web.config.debug = False
app = web.application(urls, globals())
path = os.path.abspath(os.path.dirname(__file__))
render = web.template.render(path + '/html/')
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'username': ""})


def getQR(uid,bid,action):
    data = {"uid":uid,"bid":bid,"action":action,"time":int(time.time() * 1000)}
    img = qrcode.make(str(json.dumps(data)))
    img.save(path + "/static/qr/{}-{}-{}.jpg".format(uid,bid,action))
    return "/static/qr/{}-{}-{}.jpg".format(uid,bid,action)

class index:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.index()

class bookAdds:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.bookAdd()

    def POST(self):

        data = eval(web.input().get("data"))
        print(data)
        bid = data.get("bid")
        if bid != None:
            dao.deleteBook(bid)
        title = data["title"]
        author = data["author"]
        year = data["year"]
        publisher = data["publisher"]
        isbn = data["isbn"]
        cover = data["cover"]
        introduction = data["introduction"]
        type = data["type"]
        store = data["store"]
        date = updateTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        if bid == None:
            bid = dao.getId()
        
        for i in store:
            dao.saveStoreInfo(bid,i,store[i])
        
        result = dao.saveBookDataIntoSql(bid,title,author,introduction,"-".join(type),year,str(data),date,cover,isbn,"",publisher)
        if(result):
            return json.dumps({"msg":"添加成功"})
        else:
            return json.dumps({"msg":"添加失败，这本书已存在，请检查标题"})

class jyDate:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        date= web.input().get("date")
        return json.dumps(dao.jyDate(date))

class jyCancel:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        dao.removeJy(uid,bid)
        return json.dumps({})

class bookManage:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.bookManage()


class bookSearch:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.bookSearch()

class borrowManage:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.borrowManage()

class commentManage:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.commentManage()

class face:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.face()

class ggManage:
    def GET(self):
        if session.username == "":
            raise web.seeother('/login')
        return render.gg()


class loginPage:
    def GET(self):
        return render.login()
    def POST(self):
        username = web.input().get("username")
        password = web.input().get("password")
        if admin.get(username) == password:
            session.username = username;
            return json.dumps({"result":True})
        return json.dumps({"result":False})

class userInfoManage:
    def GET(self):
        return render.userInfoManage()

class bookAdd:
    def GET(self):
        pass

class details:
    def GET(self):
        id = web.input().get("bid")
        return render.details(id)

class update:
    def GET(self):
        bid = web.input().get("bid")

        data = dao.getBookInfoById(bid)
        data = data["data"]
        data["store"] = dao.getStoreInfo(bid)
        data["bid"] = bid
        return render.update(str(data))
        
class login:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        username = web.input().get("username")
        password = web.input().get("password")
        return dao.login(username,password)

class cList:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        page = web.input().get("page")
        num = web.input().get("num")
        keyword = web.input().get("keyword")
        return dao.getCommentList(keyword,int(page),int(num))

class cRemove:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        pid = web.input().get("pid")
        return dao.removeComment(uid,bid,pid);

class addComment:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        content = web.input().get("content")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        fid = web.input().get("fid")
        intro.addBehavior(uid,bid,dct["pl"])
        return dao.addCommentToBook(bid,uid,fid,content)

class getComment:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        bid = web.input().get("id")
        page = web.input().get("page") or "1"
        return dao.getBookCommentById(bid,page)



class reg:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        username = web.input().get("username")
        password = web.input().get("password")
        nickname = web.input().get("nickname")
        sign = web.input().get("sign")
        return dao.reg(username,password,nickname,sign)

class randomList:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        length = web.input().get("length")
        return str(json.dumps(dao.getOneBookListByRandom(int(length))))

class gg:
    def GET(self):

        web.header("content-type","text/html;charset=utf-8")
        return str(json.dumps(dao.getGG()))

class bookinfo:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        id = web.input().get("id")
        return str(json.dumps(dao.getBookInfoById(id)))

class pingfen:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        bid = web.input().get("bid")
        uid = web.input().get("uid")
        star = int(web.input().get("star"))
        intro.addBehavior(uid,bid,int(star))
        return dao.addPfToBook(bid,uid,star)

class cTuijian:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        return str(dao.getCommentTj())

class bookBorrow:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        bookname = dao.getBookInfoById(bid)["data"]["title"]
        nickname = dao.getUserInfoById(uid)[0]
        getQR(uid,bid,"borrow")
        return render.borrowPage(uid,bid,bookname,nickname)

class bookBack:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        bookname = dao.getBookInfoById(bid)["data"]["title"]
        nickname = dao.getUserInfoById(uid)[0]
        getQR(uid,bid,"back")
        return render.backPage(uid,bid,bookname,nickname)

class cGeRen:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        return str(dao.getPersonalComment(uid))

class scAdd:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        bid = web.input().get("bid")
        uid = web.input().get("uid")
        intro.addBehavior(uid,bid,dct["sc"])
        return dao.scAdd(bid,uid)

class scRemove:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        bid = web.input().get("bid")
        uid = web.input().get("uid")
        return dao.scRemove(bid,uid)

class scList:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        return dao.scList(uid)

class search:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        keywords = web.input().get("keywords")
        page = int(web.input().get("page"))
        num = int(web.input().get("num"))
        return dao.search(keywords, page, num)

class jyAdd:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        storeName = web.input().get("storeName")
        startDate = web.input().get("startDate")
        endDate = web.input().get("endDate")
        intro.addBehavior(uid,bid,dct["jy"])
        return dao.jyAdd(uid, bid, storeName, startDate, endDate)

class jyChange:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        status = web.input().get("status")
        return dao.jyChange(uid, bid, status)

class userInfoChange:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        username = web.input().get("username")
        sign = web.input().get("sign")
        head = web.input().get("head")
        nickname = web.input().get("nickname")
        return json.dumps(dao.personInfoChange(username,nickname,head,sign))

class jyTotal:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        page = web.input().get("page")
        num = web.input().get("num")
        result = dao.jyTotal(uid,int(page),int(num))
        return json.dumps(result)

class jyCheck:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        action = web.input().get("action")
        result = dao.jyChange()
        return json.dumps(result)

class jyOut:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        action = web.input().get("action")
        result = dao.jyOut()
        return json.dumps(result)

class jyNotback:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        bid = web.input().get("bid")
        action = web.input().get("action")
        result = dao.jyNotback()
        return json.dumps(result)



class jyList:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        return dao.jyList(uid)

class delete:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        bid = web.input().get("bid")
        return dao.deleteBook(bid)

class bookStore:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        bid = web.input().get("bid")
        return json.dumps(dao.getStoreInfo(bid))

class ggAdd:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        title = web.input().get("title")
        content = web.input().get("content")
        return json.dumps(dao.addGG(title,content))

class removeAdd:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        id = web.input().get("id")
        return json.dumps(dao.removeGG(id))

class tjBook:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        return json.dumps(like.getSimilarBook(uid))

class tjUser:
    def GET(self):
        web.header("content-type","text/html;charset=utf-8")
        uid = web.input().get("uid")
        return json.dumps(user.getSimilarUserBookList(uid))

if __name__ == "__main__":
    app.run()
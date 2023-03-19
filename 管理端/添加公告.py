import mysql.connector as mc
import time


def addGG(title,content):
    db = mc.connect(host="39.106.51.168",user="root",passwd="wodemima",database="book")
    ch = db.cursor()
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    sql = "insert into gg (title,content,date) values ('{}','{}','{}')".format(title,content,now)
    ch.execute(sql)
    db.commit()
    db.close()

if __name__ == "__main__":
    # addGG("关于图书管理系统内部测试的公告","本次图书活动持续一周。下面给大家唱首歌。素胚勾勒出青花笔锋浓转淡，瓶身描绘的牡丹一如你初妆。冉冉檀香透过窗，心事我了然，宣纸上走笔至此搁一半。釉色渲染仕女图韵味被私藏，而你嫣然的一笑如含苞待放。你的美一缕飘散，去到我去不了的地方。天青色等烟雨，而我在等你。炊烟袅袅升起，隔江千万里。在瓶底书汉隶仿前朝的飘逸，就当我为遇见你伏笔。天青色等烟雨而我在等你，月色被打捞起晕开了结局。如传世的青花瓷自顾自美丽，你眼带笑意。")
    addGG("无关风月","啦啦啦啦啦啦")

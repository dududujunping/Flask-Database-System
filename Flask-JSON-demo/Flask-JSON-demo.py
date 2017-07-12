# coding=utf8
from flask import Flask,jsonify,request,url_for
import json
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('gbk')
app = Flask(__name__, static_url_path='')

db = MySQLdb.connect("localhost", "root", "123456", "system")
cursor = db.cursor()
cursor.execute("set names UTF8")  # 设置数据库编码。

@app.route('/', methods=['GET', 'POST'])
def index():
    return app.send_static_file('index.html')

@app.route('/sendjson',methods=['POST'])
def send_json():
    # 接收前端发来的数据,转化为Json格式,我个人理解就是Python里面的字典格式
    data = json.loads(request.get_data())

    # 然后在本地对数据进行处理,再返回给前端
    type = data["type"]
    if type == "0s":
        username = data["username"]
        passwd = data["passwd"]

        response = {"type":"0r","result":"error"}

        cursor.execute("select * from studentinfo where sno='"+username+"' and passwd='"+passwd+"'")
        student_login = cursor.rowcount;
        if student_login == 1:
            response["result"] = "student"

        cursor.execute("select * from teacherinfo where tno='"+username+"' and passwd='"+passwd+"'")
        teacher_login = cursor.rowcount;
        if teacher_login == 1:
            response["result"] = "teacher"

        cursor.execute("select * from admininfo where ano='"+username+"' and passwd='"+passwd+"'")
        admin_login = cursor.rowcount;
        if admin_login == 1:
            response["result"] = "admin"

        print username,passwd
        return jsonify(response)

    if type == "1s":
        return jsonify({"type":"1r","name":"debug"})



if __name__ == '__main__':
    app.run(host='0.0.0.0')


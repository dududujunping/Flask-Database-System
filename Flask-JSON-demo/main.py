#-*- coding: UTF-8 -*-
"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, jsonify, request, make_response, abort, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from models import Admin, Student, Teacher, Course, SC, Class, db, app

import json
import sys
reload(sys)
sys.setdefaultencoding('gbk')

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app   

app.config.from_object('config')
auth = HTTPBasicAuth()

#错误状态
@app.errorhandler(403)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({ 'error': 'Unauthorized access' }), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/', methods=['GET', 'POST'])
#@auth.login_required
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

        student_login = db.session.execute("select * from studentinfo where sno='"+username+"' and passwd='"+passwd+"'").fetchall()
        if len(student_login) == 1:
            response["result"] = "student"

        teacher_login = db.session.execute("select * from teacherinfo where tno='"+username+"' and passwd='"+passwd+"'").fetchall()
        if len(teacher_login) == 1:
            response["result"] = "teacher"

        admin_login = db.session.execute("select * from admininfo where ano='"+username+"' and passwd='"+passwd+"'").fetchall()
        if len(admin_login) == 1:
            response["result"] = "admin"

        #print username,passwd
        return jsonify(response)
    

#学生 查询功能: 根据sno获取学生信息
@app.route('/student/info/<string:sno_para>', methods = ['GET'])
def get_student(sno_para):
    if request.json["type"] == "1.1s":
        student = Student.query.filter_by(sno = sno_para).first()
        return jsonify(student.to_json())

#学生 查询功能: 根据sno获取学生成绩
@app.route('/student/grade/<string:sno_para>', methods = ['GET'])
def get_grade(sno_para):
    if request.json["type"] == "1.2s":
        gradelist = db.session.execute('SELECT cno, cname, grade FROM StudentCourse natural join CourseInfo WHERE sno = '+sno_para+';').fetchall()
        list = []
        for grade in gradelist:
            list.append({
                'cno': grade[0],
                'cname': grade[1],
                'grade': grade[2]
            })
        return jsonify({
            'type': '1.2r',
            'studentcoursecount': '%d' % len(list),
            'studentcourses': list
        })

#教师 查询功能: 根据tno获取教师信息
@app.route('/teacher/teacherInfo/<string:tno_para>', methods = ['GET'])
def get_teacher(tno_para): 
    if request.json["type"] == "2.1s":
        teacher = Teacher.query.filter_by(tno = tno_para).first()
        return jsonify(teacher.to_json())

#教师 查询功能: 根据tno获取课程信息
@app.route('/teacher/courseInfo/<string:tno_para>', methods = ['GET'])
def get_course(tno_para):
    if request.json["type"] == "2.2s":
        courselist = db.session.execute('SELECT cno, cname FROM TeacherInfo natural join CourseInfo;').fetchall()
        list = []
        for course in courselist:
            list.append({
                'cno': course[0],
                'cname': course[1]
            })
        teacher = Teacher.query.filter_by(tno = tno_para).first()
        return jsonify({
            'type': '2.2r',
            'name': teacher.tname,
            'coursecount': '%d' % len(list),
            'courses': list
        })

#教师 查询功能: 根据tno获取学生某课程的成绩
@app.route('/teacher/grade/<string:tno_para>', methods=['GET'])
def get_gradelist(tno_para):
    if request.json["type"] == "2.3s":
        gradelist = db.session.execute('SELECT cno, cname, sno, sname, grade FROM StudentInfo natural join CourseInfo natural join StudentCourse;').fetchall()
        list = []
        for grade in gradelist:
            list.append({
                'cno': grade[0],
                'cname': grade[1],
                'sno': grade[2],
                'sname': grade[3],
                'grade': grade[4]
            })
        teacher = Teacher.query.filter_by(tno = tno_para).first()
        return jsonify({
            'type': '2.3r',
            'name': teacher.tname,
            'studentcoursecount': '%d' % len(list),
            'studentcourses': list
        })

#教师 修改功能: 修改学生某课程的成绩
@app.route('/teacher/grade/<string:tno_para>', methods=['PUT'])    
def update_grade(tno_para):
    if request.json["type"] == "2.3cs":
        sclist = SC.query.filter_by(sno = request.json['sno'], cno = request.json['cno']).all()
        for sc in sclist:
            sc.grade = request.json['grade']
        db.session.commit()
        return jsonify({
            'type': '2.3cr',
            'success': 'true'
        })


#管理员 查询功能: 根据ano获取管理员信息
@app.route('/admin/info/<string:ano_para>', methods = ['GET'])
def get_admin(ano_para):
    if request.json["type"] == "3.1s":  #待修改
        admin = Admin.query.filter_by(ano = ano_para).first()
        return jsonify(admin.to_json())

#管理员 查询功能: 获取学生个人信息列表
@app.route('/admin/info/<string:ano_para>', methods = ['GET']) #待修改
def get_studentlist(ano_para):
    if request.json["type"] == "3.2s": #待修改
        studentlist = db.session.execute('SELECT * FROM StudentInfo;').fetchall()
        list = []
        for student in studentlist:
            list.append({
                'sno': student[0],
                'sname': student[1],
                'sex': student[2],
                'age': student[3],
                'classno': student[4]
            })
        return jsonify({
            'type': '3.2r',  #待修改
            'studentcount': '%d' % len(list),
            'students': list
        })

#管理员 查询功能: 获取教师个人信息列表
@app.route('/admin/info/<string:ano_para>', methods = ['GET']) #待修改
def get_teacherlist(ano_para):
    if request.json["type"] == "3.3s": #待修改
        teacherlist = db.session.execute('SELECT * FROM TeacherInfo;').fetchall()
        list = []
        for teacher in teacherlist:
            list.append({
                'tno': teacher[0],
                'tname': teacher[1],
                'sex': teacher[2],
                'age': teacher[3],
            })
        return jsonify({
            'type': '3.3r',  #待修改
            'teachercount': '%d' % len(list),
            'teachers': list
        })

#管理员 查询功能: 获取课程信息列表
@app.route('/admin/info/<string:ano_para>', methods = ['GET']) #待修改
def get_courselist(ano_para):
    if request.json["type"] == "3.4s": #待修改
        courselist = db.session.execute('SELECT * FROM CourseInfo;').fetchall()
        list = []
        for course in courselist:
            list.append({
                'cno': course[0],
                'cname': course[1],
                'tno': course[2]
            })
        return jsonify({
            'type': '3.4r',  #待修改
            'coursecount': '%d' % len(list),
            'courses': list
        })

#管理员 修改功能: 修改学生信息
@app.route('/admin/info/<string:ano_para>', methods = ['PUT']) #待修改
def update_student(ano_para):
    if request.json["type"] == "3.2cs": #待修改
        studentlist = Student.query.filter_by(sno = request.json['sno']).all() #默认sno不变
        if len(studentlist) == 0:
            abort(400) #待修改
        for student in studentlist:
            student.sname = request.json['sname']
            student.age = request.json['age']
            student.sex = request.json['sex']
            student.classno = request.json['classno']
        db.session.commit()
        return jsonify({ #待修改
            'type': '3.2cr',
            'success': 'true'
        })
    
#管理员 修改功能: 修改教师信息
@app.route('/admin/info/<string:ano_para>', methods = ['PUT']) #待修改
def update_teacher(ano_para):
    if request.json["type"] == "3.3cs": #待修改
        teacherlist = Teacher.query.filter_by(tno = request.json['tno']).all() #默认tno不变
        if len(teacherlist) == 0:
            abort(400) #待修改
        for teacher in teacherlist:
            teacher.tname = request.json['tname']
            teacher.age = request.json['age']
            teacher.sex = request.json['sex']
        db.session.commit()
        return jsonify({ #待修改
            'type': '3.3cr',
            'success': 'true'
        })

#管理员 修改功能: 修改课程信息
@app.route('/admin/info/<string:ano_para>', methods = ['PUT']) #待修改
def update_course(ano_para):
    if request.json["type"] == "3.4cs": #待修改
        courselist = Course.query.filter_by(cno = request.json['cno']).all() #默认cno不变
        if len(courselist) == 0:
            abort(400) #待修改
        for course in courselist:
            course.cname = request.json['cname']
            course.tno = request.json['tno']
        db.session.commit()
        return jsonify({ #待修改
            'type': '3.4cr',
            'success': 'true'
        })

#管理员 录入功能: 录入学生信息
@app.route('/admin/info/<string:ano_para>', methods = ['POST']) #待修改
def create_student(ano_para):
    if request.json["type"] == "3.2as": #待修改
        student = Student()
        snounique = 1
        snolist = db.session.execute('SELECT sno FROM StudentInfo;').fetchall()
        for sno in snolist:
            if request.json['sno'] == sno[0]:
                snounique = 0
        if snounique == 1:
            student.sno = request.json['sno']
            student.sname = request.json['sname']
            student.sex = request.json['sex']
            student.age = request.json['age']
            student.classno = request.json['classno']
            db.session.add(student)
            db.session.commit()
            return jsonify({ #待修改
                'type': '3.2ar',
                'success': 'true'
            })
        else:
            return jsonify({ #待修改
                'type': '3.2ar',
                'success': 'false'
            })

#管理员 录入功能: 录入教师信息
@app.route('/admin/info/<string:ano_para>', methods = ['POST']) #待修改
def create_teacher(ano_para):
    if request.json["type"] == "3.3as": #待修改
        teacher = Teacher()
        tnounique = 1
        tnolist = db.session.execute('SELECT tno FROM TeacherInfo;').fetchall()
        for tno in tnolist:
            if request.json['tno'] == tno[0]:
                tnounique = 0
        if tnounique == 1:
            teacher.tno = request.json['tno']
            teacher.tname = request.json['tname']
            teacher.sex = request.json['sex']
            teacher.age = request.json['age']
            db.session.add(teacher)
            db.session.commit()
            return jsonify({ #待修改
                'type': '3.3ar',
                'success': 'true'
            })
        else:
            return jsonify({ #待修改
                'type': '3.3ar',
                'success': 'false'
            })

#管理员 录入功能: 录入课程信息
@app.route('/admin/info/<string:ano_para>', methods = ['POST']) #待修改
def create_course(ano_para):
    if request.json["type"] == "3.4as": #待修改
        course = Course()
        cnounique = 1
        cnolist = db.session.execute('SELECT cno FROM CourseInfo;').fetchall()
        for cno in cnolist:
            if request.json['cno'] == cno[0]:
                cnounique = 0
        if cnounique == 1:
            course.cno = request.json['cno']
            course.cname = request.json['cname']
            course.tno = request.json['tno']
            db.session.add(course)
            db.session.commit()
            return jsonify({ #待修改
                'type': '3.4ar',
                'success': 'true'
            })
        else:
            return jsonify({ #待修改
                'type': '3.4ar',
                'success': 'false'
            })

#管理员 删除功能: 删除学生信息
@app.route('/admin/info/<string:ano_para>', methods = ['DELETE']) #待修改
def delete_student(ano_para):
    if request.json["type"] == "3.2ds": #待修改
        student = Student.query.filter_by(sno = request.json['sno']).first()
        db.session.delete(student)
        db.session.commit()
        return jsonify({ #待修改
            'type': '3.2dr',
            'success': 'true'
        })

#管理员 删除功能: 删除教师信息
@app.route('/admin/info/<string:ano_para>', methods = ['DELETE']) #待修改
def delete_teacher(ano_para):
    if request.json["type"] == "3.3ds": #待修改
        teacher = Teacher.query.filter_by(tno = request.json['tno']).first()
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({ #待修改
            'type': '3.3dr',
            'success': 'true'
        })

#管理员 删除功能: 删除课程信息
@app.route('/admin/info/<string:ano_para>', methods = ['DELETE']) #待修改
def delete_course(ano_para):
    if request.json["type"] == "3.4ds": #待修改
        course = Course.query.filter_by(cno = request.json['cno']).first()
        db.session.delete(course)
        db.session.commit()
        return jsonify({ #待修改
            'type': '3.4dr',
            'success': 'true'
        })
'''
@app.route('/students/<int:sno>', methods = ['GET'])
def get_grade(sno_para):
    student = SC.query.filter_by(sno = sno_para).all()
    list = []
    for tmp in student:
        list.append(tmp.to_json())
    return 
'''

'''    
@app.route('/login')
@auth.login_required
def get_resource():
    return jsonify({'data': 'Hello, %s!' % g.user.id})

@auth.get_password
def get_password(id):
    user = User.query.filter_by(id = id).first()
    if not user:
        return False
    g.user = user
    return g.user.password


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

#获取学生列表
@app.route('/students', methods = ['GET'])
def get_stulist():
    return jsonify({'students': s})

#根据学号获取学生信息
@app.route('/students/<int:no>', methods = ['GET'])
def get_student(no):
    student = filter(lambda s: s['sno'] == no, students)
    if len(student) == 0:
        abort(404)
    return jsonify({'student': student[0]})

#添加一个学生
@app.route('/students', methods = ['POST'])
def add_student():
    if not request.json or not ('sno' or 'sname' or 'sex') in request.json:
        abort(400)
    student = {
        'sno': request.json['sno'],
        'sname': request.json['sname'],
        'sex': request.json['sex'],
        'grade': request.json.get('grade', "")
    }
    students.append(student)
    return jsonify({'student': student}), 201

#根据学号修改学生信息
@app.route('/students/<int:no>', methods = ['PUT'])
def update_student(no):
    student = filter(lambda s: s['sno'] == no, students)
    if len(student) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'sname' in request.json and type(request.json['sname']) is not unicode:
        abort(400)
    if 'sex' in request.json and type(request.json['sex']) is not unicode:
        abort(400)
    if 'grade' in request.json and type(request.json['grade']) is not int:
        abort(400)
    student[0]['sname'] = request.json.get('sname', student[0]['sname'])
    student[0]['sex'] = request.json.get('sex', student[0]['sex'])
    student[0]['grade'] = request.json.get('grade', student[0]['grade'])
    return jsonify({'student': student[0]})

#根据学号删除学生信息
@app.route('/students/<int:no>', methods = ['DELETE'])
def delete_student(no):
    student = filter(lambda s: s['sno'] == no, students)
    if len(student) == 0:
        abort(404)
    students.remove(student[0])
    return jsonify({'result': True})
'''

if __name__ == '__main__':
    #import os
    #HOST = os.environ.get('SERVER_HOST', 'localhost')
    #try:
    #    PORT = int(os.environ.get('SERVER_PORT', '5555'))
    #except ValueError:
    #    PORT = 5555
    app.run(debug = True)

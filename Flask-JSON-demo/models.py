#-*- coding: UTF-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
db = SQLAlchemy(app)

class Admin(db.Model):
    __tablename__ = 'AdminInfo'
    ano = db.Column(db.String(20), primary_key = True)
    passwd = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return "<Admin(ano = '%s')>" % self.ano
    
    def to_json(self):
        return {
            'ano': self.ano,
            #'passwd': self.passwd
        }

class SC(db.Model):
    __tablename__ = 'StudentCourse'
    sno = db.Column(db.String(20), db.ForeignKey('StudentInfo.sno'), primary_key = True)
    cno = db.Column(db.String(20), db.ForeignKey('CourseInfo.cno'), primary_key = True)
    grade = db.Column(db.String(20), nullable = True)
    #...
    #def __repr__(self):
    #    return '<StudentCourse %r>' % self.id

    def to_json(self):
        return {'grade': self.grade}

class Student(db.Model):
    __tablename__ = 'StudentInfo'
    sno = db.Column(db.String(20), primary_key = True)
    sname = db.Column(db.String(50), nullable = False)
    sex = db.Column(db.String(20), nullable = False)
    age = db.Column(db.String(3), nullable = False)
    classno = db.Column(db.String(20), db.ForeignKey('ClassInfo.classno'))
    passwd = db.Column(db.String(20), nullable = False) 
    course = db.relationship('SC', foreign_keys = [SC.sno], backref = db.backref('student', lazy = 'joined'), lazy = 'dynamic')
    #...
    def __repr__(self):
        return "<Student(sno='%s', sname='%s')>" % (self.sno, self.sname)

    def to_json(self):
        return {
            'type': '1.1r',
            'name': self.sname,
            'sno': self.sno,
            'sname': self.sname,
            'sex': self.sex,
            'age': self.age,
            'classno': self.classno
        }

class Teacher(db.Model):
    __tablename__ = 'TeacherInfo'
    tno = db.Column(db.String(20), primary_key = True)
    tname = db.Column(db.String(50), nullable = False)
    sex = db.Column(db.String(20), nullable = False)
    age = db.Column(db.String(3), nullable = False)
    passwd = db.Column(db.String(20), nullable = False)
    students = db.relationship('Course', backref = 'teacher', lazy = 'dynamic')
    #...
    def __repr__(self):
        return "<Teacher(tno='%s', tname='%s')>" % (self.tno, self.tname)

    def to_json(self):
        return {
            'type': '2.1r',
            'name': self.tname,
            'tno': self.tno,
            'tname': self.tname,
            'sex': self.sex,
            'age': self.age,
        }

class Course(db.Model):
    __tablename__ = 'CourseInfo'
    cno = db.Column(db.String(20), primary_key = True)
    cname = db.Column(db.String(50), nullable = False)
    tno = db.Column(db.String(20), db.ForeignKey('TeacherInfo.tno'))  
    student = db.relationship('SC', foreign_keys = [SC.cno], backref = db.backref('course', lazy = 'joined'), lazy = 'dynamic')
    #...
    def __repr__(self):
        return "<Course(cno='%s', cname='%s')>" % (self.cno, self.cname)

    def to_json(self):
        return {
            'cno': self.cno,
            'cname': self.cname,
        }

class Class(db.Model):
    __tablename__ = 'ClassInfo'
    classno = db.Column(db.String(20), primary_key = True)
    major = db.Column(db.String(50), nullable = False)
    students = db.relationship('Student', backref = 'class', lazy = 'dynamic')
    #...
    def __repr__(self):
        return "<Class(classno='%s', major='%s')>" % (self.classno, self.major)

    def to_json(self):
        return {
            'classno': self.classno,
            'major': self.major
        }

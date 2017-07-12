#-*- coding: UTF-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@localhost:3306/system'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

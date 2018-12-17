#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: config.py
@time: 2018/11/27 下午5:57
@desc:

'''
import os
from datetime import timedelta
from celery.schedules import crontab


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'g78gf7d8g7fd98g79df8hgaf7a'
    # SECRET_KET = os.environ.get('SECRET_KET')
    FLASK_ADMIN = 'xxxx@163.com'

    @staticmethod
    def init_app(app):
        pass

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')

class DevelopmentConfig(Config):

    DEBUG=True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/flaskcg_demo'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # celery
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    # using darabase to store task state and result
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    # sqlite (filename) CELERY_RESULT_BACKEND = ‘db+sqlite:///results.sqlite’
    # mysql CELERY_RESULT_BACKEND = ‘db+mysql://scott:tiger@localhost/foo’
    # postgresql CELERY_RESULT_BACKEND = ‘db+postgresql://scott:tiger@localhost/mydatabase’
    # oracle CELERY_RESULT_BACKEND = ‘db+oracle://scott:tiger@127.0.0.1:1521/sidname’
    CELERY_TIMEZONE = 'Asia/Shanghai'
    CELERY_IMPORT = (
        'celery_app.task1',
        'celery_app.task2',
    )

    CELERYBEAT_SCHEDULE = {
        'task1': {
            'task': 'celery_app.task1.add',
            'schedule': timedelta(seconds=10),  # 执行策略, 每隔10s执行一次
            'args': (4, 8)
        },
        'task2': {
            'task': 'celery_app.task2.mutiply',
            'schedule': crontab(hour=15, minute=30),  # 执行策略, 定时任务
            'args': (3, 7)
        }
    }


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                               'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
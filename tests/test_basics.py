#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: test_basics.py
@time: 2018/11/30 下午4:47
@desc:

'''
import unittest
from flask import current_app
from app import create_app

class BasicTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('development')
        self.app_content = self.app.app_context()
        self.app_content.push()
        #db.create_all()

    def test_app_is_dev(self):
        self.assertTrue(current_app.config['DEVELOPMENT'])

    def test_app_exist(self):
        self.assertFalse(current_app is None)
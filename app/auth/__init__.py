#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: __init__.py.py
@time: 2018/11/29 下午5:00
@desc:

'''

from flask import Blueprint

auth = Blueprint('auth', __name__)
from . import views, errors, forms
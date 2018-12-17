#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: __init__.py.py
@time: 2018/11/29 下午2:13
@desc:

'''

from flask import Blueprint
from ..models import Permission

main = Blueprint('main', __name__)
from . import views, errors

@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)
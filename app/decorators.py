#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: decorators.py
@time: 2018/12/4 上午11:19
@desc:

'''
from flask_login import current_user
from functools import wraps

from flask import abort
from .models import Permission
def permission_required(permission):
    def decorate(f):
        @wraps(f)
        def decorate_function(*args, **kwargs):
            if current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorate_function
    return decorate

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

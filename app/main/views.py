#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: views.py
@time: 2018/11/29 下午4:57
@desc:

'''

from flask import render_template, session, redirect, url_for
from .. import db
from . import main
from .forms import NameForm
from ..models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            print("新增用户----->{}".format(user))
        else:
            session['known'] = True

        session['user'] = form.name.data
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, username = session.get('name'),
                           known = session.get('known',False))



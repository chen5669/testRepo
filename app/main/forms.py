#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: forms.py
@time: 2018/11/29 下午4:57
@desc:

'''

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class NameForm(FlaskForm):
    name = StringField('???', validators=[DataRequired()])

    submit = SubmitField('Submit')
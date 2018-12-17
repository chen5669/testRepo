#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: forms.py
@time: 2018/11/29 下午5:01
@desc:

'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo, Regexp
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegisterFrom(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, numbers, dots or '
                                                          'underscores')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    sumbit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username =field.data).first():
            raise ValidationError('Username Already in use!')

    def validate_email(self, field):
        if User.query.filter_by(user_email = field.data).first():
            raise ValidationError('Email already registered!')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Password must be match.')])
    password2 = PasswordField('Confirmed New Password', validators=[DataRequired()])
    submit = SubmitField('Update Password')

class PasswordResetRequestFrom(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    submit = SubmitField('Reset Password')

class PasswordRsetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='password must be match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address!')

    def validate_email(self, field):
        if User.query.filter_by(user_email = field.data).first():
            raise ValidationError('Email already registered.')

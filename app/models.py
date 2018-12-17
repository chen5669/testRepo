#!/usr/bin/env python
# encoding: utf-8

'''
@author: cgsnd
@file: models.py
@time: 2018/11/29 下午4:43
@desc:

'''
from app import db, create_app
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from . import login_manager
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Permission:
    FOLLOW = 1 #关注
    COMMENT =2 #发表
    WRITE = 4
    MODETARE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0
    @staticmethod
    def insert_roles():
        roles = {
            'User':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODETARE],
            'Administrator':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE,
                             Permission.MODETARE, Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_perssions()
            for perm in role[r]:
                role.add_permissions(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()



    def add_permissions(self, perm):
        if not self.has_permissions(perm):
            self.has_permissions += perm

    def remove_permissions(self, perm):
        if self.has_permissions(perm):
            self.permissions -= perm

    def reset_perssions(self):
        self.permissions = 0

    def has_permissions(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    role_id =db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    user_email = db.Column(db.String(128), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    content = db.Column(db.String(200))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.TEXT)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.user_email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({"confirm":self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset':self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_mail': new_email}).decode('utf-8')

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('change_email') !=self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(user_email=new_email).first() is not None:
            return False
        self.user_email = new_email
        db.session.commit()
        return True

    def can(self, perm):
        return self.role is not None and self.role.has_permissions(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User %r>'% self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# if __name__ == '__main__':
#     app = create_app('dev')
#     app_content = app.app_context()
#     with app_content:
#         db.create_all()
#     #添加角色
#         role = Role(
#             name="超级管理员",
#         )
#         db.session.add(role)
#         db.session.commit()
#
#         #添加管理员
#         #对密码加密保存
#         #from werkzeug.security import generate_password_hash
#
#         admin = User(
#             username="admin",
#         )
#         db.session.add(admin)
#         db.session.commit()



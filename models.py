from . import db
from flask import redirect, url_for
from flask_admin import AdminIndexView

from flask_login import UserMixin,current_user,login_user,logout_user
# from . import admin
from flask_admin.contrib.sqla import ModelView


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Admindb(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):

        return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('auth.adminlogin'))


class MyModelView(ModelView):
    def is_accessible(self):


        return current_user.is_authenticated

    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('auth.adminlogin'))

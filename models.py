from . import db
from flask import redirect, url_for
from flask_admin import AdminIndexView

from flask_login import UserMixin,current_user,login_user,logout_user

from flask_admin.contrib.sqla import ModelView




#---------------------- USER CREDENTIALS--------------------------#

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))



#----------------------ADMIN CREDENTIALS----------------------------#

class Admindb(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))




#----------------------FEEDBACK TABLE-------------------------------#

class Feedback(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    message = db.Column(db.String(1000))




#-----------------------VIEWS FOR ADMINPAGE----------------------------#


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



#----------------------------FILE STORAGE-------------------------------#


class Image(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    img_filename = db.Column(db.String())
    img_data = db.Column(db.LargeBinary)
def add_image(image_dict):
    new_image = Image(name=image_dict['name'], \
                        img_filename=image_dict['img_filename'], \
                        img_data=image_dict['img_data'])
    db.session.add(new_image)
    db.session.commit()

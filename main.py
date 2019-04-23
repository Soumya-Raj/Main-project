import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,Blueprint,flash,send_file
from werkzeug import secure_filename
#from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_required, current_user
from flask_mail import Mail,Message

from . import db,mail
from .models import Image,add_image,Feedback

main = Blueprint('main',__name__)
global UPLOAD_FOLDER


MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'lungvison'
MAIL_PASSWORD = 'qweasdzxc@123'

ADMINS = ['lungvison@gmail.com']




@main.route('/')
def index():
#-------------CODE FOR THE COUNTERS IN HOME PAGE----------
    sql_image='select count(img_filename) from Image'
    count_file = db.session.execute(sql_image)

    d, a = {}, []
    for rowproxy in count_file:

        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
            a.append(d[column])

    if(a):
        flash(a[0],'upload_count')
    else:
        flash('ooombi')

    sql_users='select count(email) from User'
    count_file = db.session.execute(sql_users)

    for rowproxy in count_file:

        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
            a.append(d[column])

    if(a):
        flash(a[1],'account_count')
    else:
        flash('ooombi')




    return render_template('main.html')

@main.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@main.route('/process_email', methods=['POST'])
def process_email():

    email = request.form.get('email')
    name = request.form.get('name')
    message = request.form.get('message')

    user = Feedback.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user:
        flash('To preserve the genuinity of feedbacks,a user can send only 1 feedback','feedback') # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('main.index'))

    feed=Feedback(email=email,name=name,message=message)

    db.session.add(feed)
    db.session.commit()


    return redirect(url_for('main.index'))

@main.route('/startanalysis')
@login_required
def startanalysis():
    return redirect(url_for('main.uploadit'))


@main.route('/uploadit', methods=['POST','GET'])
# @login_required

def uploadit():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files.getlist("file[]"):
        #     flash('No file part')
        #     return redirect(request.url)
        uploaded_files = request.files.getlist("file[]")
        filenames = []
        for file in uploaded_files:
        # if user does not select file, browser also
        # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                add_image({
                            'name': current_user.name,
                            'img_filename' : filename ,
                            'img_data' : file.read(),
                            })

                # file.save(os.path.join(UPLOAD_FOLDER, filename))
                filenames.append(filename)
        return redirect(url_for('main.uploadit',
                                filename=filename))
    return render_template('upload.html')

@main.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(UPLOAD_FOLDER,
                               filename)
# @main.route('/login',methods=['POST','GET'])
# def login():
#     return render_template('login.html')


# if __name__ == '__main__':
#     main.run(debug = True)

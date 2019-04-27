import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,Blueprint,flash,send_file
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_required, current_user


from . import db,mail
from .models import Image,add_image,Feedback

main = Blueprint('main',__name__)



@main.route('/')
def index():
#-------------CODE FOR THE COUNTERS IN HOME PAGE----------
    sql_image='select count(img_filename) from Image'
    count_file = db.session.execute(sql_image)

    d, a, mes, nam = {}, [], [], []

    i=0
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

    sql_feedback='select message as m from Feedback'
    count_file = db.session.execute(sql_feedback)


    for rowproxy in count_file:

        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
            mes.append(d[column])



        while(i<len(mes)):

            category='message'+str(i)

            flash(mes[i],category)
            i+=1


    sql_feedback_name='select name as n from Feedback'
    count_file = db.session.execute(sql_feedback_name)


    for rowproxy in count_file:

        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for column, value in rowproxy.items():
            # build up the dictionary
            d = {**d, **{column: value}}
            nam.append(d[column])

        i=0
        while(i<len(nam)):

            category='name'+str(i)

            flash(nam[i],category)
            i+=1



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

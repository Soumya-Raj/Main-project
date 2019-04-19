import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,Blueprint,flash,send_file
from werkzeug import secure_filename
#from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,login_required, current_user


main = Blueprint('main',__name__)
global UPLOAD_FOLDER
UPLOAD_FOLDER= '/home/rakshith/Desktop/'


@main.route('/')
def index():
    return render_template('main.html')
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
                file.save(os.path.join(UPLOAD_FOLDER, filename))
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

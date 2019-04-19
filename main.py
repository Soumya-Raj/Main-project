import os
from flask import render_template, request, redirect, url_for, send_from_directory,Blueprint,flash,send_file
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
    return render_template('upload.html')

@main.route('/uploadit', methods=['POST'])
# @login_required
def uploadit():

    # Get the name of the uploaded files
    if request.method == 'POST':
        uploaded_files = request.files['file']
        filenames = []
        ALLOWED_EXTENSIONS=['raw', 'mhd']




        for file in uploaded_files:

            # Check if the file is one of the allowed types/extensions
            # and file.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
            if file :
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                filenames.append(filename)
                return render_template('main.html')

    return render_template('admin_login.html')

@main.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(UPLOAD_FOLDER,
                               filename)
# @main.route('/login',methods=['POST','GET'])
# def login():
#     return render_template('login.html')


# if __name__ == '__main__':
#     main.run(debug = True)

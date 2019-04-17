import os
from flask import render_template, request, redirect, url_for, send_from_directory,Blueprint
from werkzeug import secure_filename
#from . import db
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

main = Blueprint('main',__name__)


@main.route('/')
def index():
    return render_template('main.html')

@main.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)

    return render_template('upload.html', filenames=filenames)

@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
# @main.route('/login',methods=['POST','GET'])
# def login():
#     return render_template('login.html')


# if __name__ == '__main__':
#     main.run(debug = True)

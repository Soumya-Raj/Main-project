# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_dropzone import Dropzone


# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
dropzone = Dropzone()



def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['UPLOAD_FOLDER'] = '/home/sou/Desktop/web/uploads'
    # These are the extension that we are accepting to be uploaded
    app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'dcm', 'raw', 'mhd'])

    app.config.update(


        DROPZONE_MAX_FILE_SIZE=3000,
        DROPZONE_ALLOWED_FILE_TYPE='.mhd ',
        DROPZONE_MAX_FILES=2,

        SECRET_KEY = 'poilkjmnb',

    )

    # For a given file, return whether it's an allowed type or not

    db.init_app(app)
    dropzone.init_app(app)


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)




    from .models import User,MyModelView,Admindb,MyAdminIndexView
    admin=Admin(app,index_view=MyAdminIndexView())
    admin.add_view(MyModelView(User,db.session))
    admin.add_view(MyModelView(Admindb,db.session))


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# def allowed_file(filename):
#     return '.' in filename and
#            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

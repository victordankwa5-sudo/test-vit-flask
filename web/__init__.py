from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    global mail
    mail = Mail(app)
    app.config['SECRET_KEY'] = "^k;'df/c^$*3,2*(#@&)"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'victordankwa5@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jfsd mfix jrzg mvar'
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)
    db.init_app(app)
    
    from.views import views
    from .auth import auth
    from .admin import admin
    from .admin_views import admin_views
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')
    app.register_blueprint(admin_views, url_prefix='/')
    
    from .models import User
    
    with app.app_context():
        create_db()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_db():
    if not path.exists('web/' + DB_NAME):
        db.create_all()
from flask import Flask, redirect, url_for
from os import path
import mysql.connector
from .config import Config,API_ADDRESS
from flask_login import LoginManager,UserMixin,logout_user
import requests

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    from .models import User

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(tokenandfernetkey):
        access_token_start_index = tokenandfernetkey.find('access_token:') + len('access_token:')
        fernet_key_start_index = tokenandfernetkey.find('fernet_key:') + len('fernet_key:')
        token = tokenandfernetkey[access_token_start_index:fernet_key_start_index - len('fernet_key:')].strip()
        fernetKey = tokenandfernetkey[fernet_key_start_index:].strip()

        url = f'{API_ADDRESS}/users/me/info'
        headers = {'accept': 'application/json','Authorization': f'bearer {token}'}
        req = requests.get(url, headers=headers)
        user = req.json()
        return User(tokenandfernetkey,token=token,fernetKey=fernetKey,username=user['username'],email=user['email'],userid=user['id'])

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('views.login'))

    return app

def createTables():
    cursor = db.cursor()
    cursor.execute('CREATE TABLE if not exists Users (id INT PRIMARY KEY AUTO_INCREMENT,email VARCHAR(150) UNIQUE,password VARCHAR(150));')
    cursor.execute('CREATE TABLE if not exists Data (userId INT,FOREIGN KEY(userId) REFERENCES Users(id),info VARCHAR(150));')
    cursor.close()
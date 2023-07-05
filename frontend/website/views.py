import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import login_user,login_required,logout_user,current_user
from .config import API_ADDRESS
from .models import User

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def index():
    return render_template("index.html",user=current_user)

@views.route('/login', methods=['GET', 'POST'])
def login():
    session_data = {}
    if current_user.is_authenticated:
        return redirect(url_for('views.index'))
    if request.method == 'POST':
        formType = request.form.get('form_type')
        if formType == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            session['session_data'] = {
            'username': username,
            }
            url = f'{API_ADDRESS}/login'
            headers = {'accept': 'application/json','Content-Type': 'application/x-www-form-urlencoded'}
            info = f'grant_type=&username={username}&password={password}&scope=&client_id=&client_secret='
            response = requests.post(url, headers=headers,data=info)
            json = response.json()
            if 'status' in json and json['status'] == True:
                tokenandfernetkey = 'access_token:' + json['access_token'] + 'fernet_key:' + json['fernet_key']
                user = User(tokenandfernetkey)
                login_user(user,remember=False)
                flash('Logged in.', category='success')
                session.pop('session_data', None)
                return redirect(url_for('views.index'))
            else:
                session_data = session.get('session_data', {})
                if 'message' in json:
                    flash(json['message'],category='error')
                else:
                    flash('An error occurred while logging in.',category='error')
        elif formType == 'register':
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')

            session['session_data'] = {
            'username': username,
            'email': email,
            }

            url = f'{API_ADDRESS}/createAccount'
            headers = {'accept': 'application/json','Content-Type': 'application/json'}
            info = f'{{"username": "{username}","email": "{email}","password": "{password}"}}'
            response = requests.post(url, headers=headers,data=info)
            json = response.json()
            if 'status' in json and json['status'] == True:
                flash(json['message'] + ' Please Login.', category='success')
                session.pop('session_data', None)
                return redirect(url_for('views.login') + '#')
            else:
                session_data = session.get('session_data', {})
                if 'message' in json:
                    flash(json['message'],category='error')
                else:
                    flash('An error occurred while creating your account.',category='error')
    return render_template("login.html", user=current_user , session_data=session_data)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', category='success')
    return redirect(url_for('views.index'))

@views.route('/dashboard/passwords', methods=['GET', 'POST'])
@login_required
def dash_passwords():
    if request.method == 'POST':
        formType = request.form.get('form_type')
        if formType == 'new':
            print('This is a test')
            service = request.form.get('service')
            username = request.form.get('username')
            password = request.form.get('password')
            notes = request.form.get('notes')
            json = current_user.newPassword(service,username,password,notes)
            print(json)
            if 'status' in json and json['status']:
                flash(json['message'], category='success')
                return redirect(url_for('views.dash_passwords'))
            else:
                if 'message' in json:
                    flash(json['message'], category='error')
                else:
                    flash('An error occurred while trying to add the password.', category='error')
        elif formType == 'edit':
            passId = request.form.get('passId')
            service = request.form.get('service')
            username = request.form.get('username')
            password = request.form.get('password')
            notes = request.form.get('notes')
            json = current_user.editPassword(passId,service,username,password,notes)
            if 'status' in json and json['status']:
                flash(json['message'], category='success')
                return redirect(url_for('views.dash_passwords'))
            else:
                if 'message' in json:
                    flash(json['message'], category='error')
                else:
                    flash('An error occurred while trying to edit the password.', category='error')
    return render_template("dash_passwords.html",user=current_user)

@views.route('/delete-pass')
@login_required
def delete_pass():
    passId = request.args.get('passId')
    json = current_user.delPassword(passId)
    if 'status' in json and json['status']:
        flash(json['message'], category='success')
    else:
        if 'message' in json:
            flash(json['message'], category='error')
        else:
            flash('An error occurred while trying to delete the password.', category='error')
    return redirect(url_for('views.dash_passwords'))
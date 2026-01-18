from flask import Blueprint, render_template, request, session, redirect, url_for
from db import db
from db.models import users, articles
from werkzeug.security import generate_password_hash

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8')
def main():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login or not password:
        return render_template('lab8/register.html', error='Заполните все поля')

    existing_user = users.query.filter_by(login=login).first()
    if existing_user:
        return render_template('lab8/register.html', error='Такой логин уже существует')

    hashed_password = generate_password_hash(password)

    new_user = users(login=login, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/lab8/login')
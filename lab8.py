from flask import Blueprint, render_template, request, session, redirect, url_for
from db import db
from db.models import users, articles
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, login_user, current_user

lab8 = Blueprint('lab8', __name__, template_folder='templates')

@lab8.route('/lab8')
def main():
    login = session.get('login', None)
    return render_template('lab8/lab8.html', login=login)

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

    login_user(new_user)

    return redirect('/lab8')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    remember = request.form.get('remember') == 'on'  # True, если галочка стоит

    if not login or not password:
        return render_template('lab8/login.html', error='Заполните все поля')

    user = users.query.filter_by(login=login).first()

    if not user or not check_password_hash(user.password, password):
        return render_template('lab8/login.html', error='Неверный логин или пароль')

    login_user(user, remember=remember)  # ← передаём remember
    return redirect('/lab8')

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/create.html', error='Заполните все поля')

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text
    )
    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/list')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first_or_404()

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab8/edit.html', article=article, error='Заполните все поля')

    article.title = title
    article.article_text = article_text
    db.session.commit()

    return redirect('/lab8/list')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first_or_404()
    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/list')

@lab8.route('/lab8/list')
@login_required
def list_articles():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/list.html', articles=user_articles)
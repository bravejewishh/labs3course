from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path 

lab5 = Blueprint('lab5', __name__, template_folder='templates')

# Функции для работы с БД
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='polina_penkova_knowledge_base',
            user='polina_penkova_knowledge_base',
            password='555'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    if conn and cur:
        conn.commit()
        cur.close()
        conn.close()

def execute_query(cur, query, params=None):
    """Универсальная функция для выполнения запросов в PostgreSQL и SQLite"""
    if current_app.config['DB_TYPE'] == 'postgres':
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
    else:
        # Для SQLite заменяем %s на ?
        if params:
            query = query.replace('%s', '?')
            cur.execute(query, params)
        else:
            cur.execute(query)

# Routes
@lab5.route('/lab5')
def main():
    return render_template('lab5/lab5.html', login=session.get('login'))

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    if conn is None or cur is None:
        return render_template('lab5/register.html', error='Ошибка подключения к БД')
    
    try:
        # Проверка существующего пользователя
        execute_query(cur, "SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', 
                                 error='Такой пользователь уже существует')
        
        # Создание нового пользователя
        password_hash = generate_password_hash(password)
        execute_query(cur, "INSERT INTO users (login, password) VALUES (%s, %s);", 
                    (login, password_hash))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
        
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/register.html', 
                             error=f'Ошибка при регистрации: {str(e)}')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    if conn is None or cur is None:
        return render_template('lab5/login.html', error='Ошибка подключения к БД')
    
    try:
        # Поиск пользователя
        execute_query(cur, "SELECT * FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        # Проверка пароля
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        # Сохранение в сессии
        session['login'] = login
        session['user_id'] = user['id']
        
        db_close(conn, cur)
        return render_template('lab5/success_login.html', login=login)
        
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/login.html', error=f'Ошибка при входе в систему: {str(e)}')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create_article():
    if 'login' not in session:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not (title and article_text):
        return render_template('lab5/create_article.html', error='Заполните все поля')

    conn, cur = db_connect()

    try:
        # Получаем ID пользователя
        execute_query(cur, "SELECT id FROM users WHERE login=%s;", (session['login'],))
        user = cur.fetchone()
        login_id = user["id"]

        # Создаем статью
        execute_query(cur, "INSERT INTO articles (login_id, title, article_text) VALUES (%s, %s, %s);", 
                     (login_id, title, article_text))

        db_close(conn, cur)
        return redirect('/lab5')
    
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error=f'Ошибка при создании статьи: {str(e)}')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    try:
        # Получаем ID пользователя
        execute_query(cur, "SELECT id FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        login_id = user["id"]

        # Получаем статьи
        execute_query(cur, "SELECT * FROM articles WHERE login_id=%s;", (login_id,))
        articles = cur.fetchall()

        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=articles)
    
    except Exception as e:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', error=f'Ошибка при загрузке статей: {str(e)}')

@lab5.route('/lab5/logout')
def logout():
    session.clear()
    return redirect('/lab5')
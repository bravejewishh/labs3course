from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path 

lab5 = Blueprint('lab5', __name__, template_folder='templates')

# Функции для работы с БД - ДОЛЖНЫ БЫТЬ ПЕРЕД ВСЕМИ ROUTE'ами
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
        print("DEBUG: Подключение к БД закрыто")

# Теперь все route'ы - после определения функций

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
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', 
                                 error='Такой пользователь уже существует')
        
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", 
                    (login, password_hash))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
        
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/register.html', 
                             error=f'Ошибка при регистрации: {str(e)}')

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():  # Исправьте имя функции обратно
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    print(f"DEBUG: Получены данные: login={login}, password={password}")
    
    if not (login and password):
        return render_template('lab5/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    if conn is None or cur is None:
        return render_template('lab5/login.html', error='Ошибка подключения к БД')
    
    try:
        # Поиск пользователя
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        user = cur.fetchone()
        
        print(f"DEBUG: Найден пользователь: {user}")
        
        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        # Проверка пароля
        print(f"DEBUG: Проверяем пароль. Хеш в БД: {user['password']}")
        
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        # Сохранение в сессии
        session['login'] = login
        session['user_id'] = user['id']
        
        db_close(conn, cur)
        print("DEBUG: Успешный вход!")
        return render_template('lab5/success_login.html', login=login)
        
    except Exception as e:
        print(f"DEBUG: Ошибка при входе: {str(e)}")
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

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users WHERE login=%s;", (session['login'], ))
    login_id = cur.fetchone()["id"]

    cur.execute(f"INSERT INTO articles(user_id, title, article_text) VALUES ('{login_id}', '{title}', '{article_text}');")

    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()
    
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    login_id = cur.fetchone()["id"]

    cur.execute(f"SELECT * FROM articles WHERE user_id='{login_id}';")
    articles = cur.fetchall()

    db_close(conn, cur)
    return render_template('/lab5/articles.html', articles=articles)


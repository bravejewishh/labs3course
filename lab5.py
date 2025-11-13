from flask import Blueprint, render_template, request, redirect, session
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/login')
def login():
    return "Страница входа"

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='polina_penkova_knowledge_base',
        user='polina_penkova_knowledge_base',
        password='555'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', 
                             error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password)
    cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", 
                (login, password_hash))
    

    conn.commit()
    cur.close()
    conn.close()
    
    return render_template('lab5/success.html', login=login)
    if not (login or password):
        return render_template('lab5/register.html', error='заполните все поля')

@lab5.route('/lab5/list')
def list_articles():
    return "Список статей"

@lab5.route('/lab5/create')
def create_article():
    return "Создать статью"
from flask import Flask, url_for, request, redirect, make_response, abort, render_template, session, current_app
import datetime
import os 
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7

app = Flask (__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'самый страшный секрет на свете')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)

@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background-color: #f8f9fa;
            }
            h1 {
                color: #dc3545;
            }
            .error-box {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                display: inline-block;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="error-box">
            <h1>500 - Внутренняя ошибка сервера</h1>
            <p>На сервере произошла непредвиденная ошибка.</p>
            <p>Мы уже работаем над устранением проблемы.</p>
            <a href="/">Вернуться на главную</a>
        </div>
    </body>
</html>''', 500

@app.route('/test_500')
def test_500():
    x = 1 / 0
    return "Этот код никогда не выполнится"

@app.route('/test_500_2')
def test_500_2():
    x = 5 + "строка"
    return "Этот код тоже никогда не выполнится"

@app.errorhandler(404)
def not_found(err):
    css_path = url_for("static", filename="lab1/404.css")
    image_path = url_for("static", filename="lab1/404.jpg")
    
    return '''
<!doctype html>
<html>
    <head>
        <title>страница не найдена</title>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>404</h1>
        <p>страница не найдена :((</p>
        <img src="''' + image_path + '''">
        <br>
        <a href="/">На главную</a>
    </body>
</html>''', 404

@app.errorhandler(400)
def bad_request(err):
    return "неправильный запрос((((", 400

@app.errorhandler(401)
def unauthorized(err):
    return "требуется авторизация((((", 401


@app.errorhandler(403)
def forbidden(err):
    return "доступ запрещен((((", 403

@app.errorhandler(405)
def method_not_allowed(err):
    return "метод не разрешен((((", 405


class PaymentRequired(Exception):
    code = 402
    description = 'требуется оплата(((('

class Teapot(Exception):
    code = 418
    description = 'я чайник!(((('

@app.errorhandler(PaymentRequired)
def payment_required(err):
    return err.description, err.code

@app.errorhandler(Teapot)
def teapot(err):
    return err.description, err.code

@app.route("/")
@app.route("/index")
def index():
    return """<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <main>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3">Третья лабораторная</a></li>
                <li><a href="/lab4">Четвертая лабораторная</a></li>
                <li><a href="/lab5">Пятая лабораторная</a></li>
                <li><a href="/lab6">Шестая лабораторная</a></li>
                <li><a href="/lab7">Седьмая лабораторная</a></li>
                <li><a href="/lab8">Восьмая лабораторная</a></li>
            </ul>
        </main>
        <footer>
            Пенькова Полина Александровна, ФБИ-34, 3 курс, 2025
        </footer>
    </body>
</html>"""


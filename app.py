from flask import Flask, url_for, request, redirect, make_response, abort, render_template
import datetime
app = Flask (__name__)

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
    css_path = url_for("static", filename="404.css")
    image_path = url_for("static", filename="404.jpg")
    
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
            </ul>
        </main>
        <footer>
            Пенькова Полина Александровна, ФБИ-34, 3 курс, 2025
        </footer>
    </body>
</html>"""

@app.route("/lab1")
def lab1():
    return """<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые ба-
            зовые возможности.
        </p>
        <a href="/">На главную</a>
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/">Главная страница (/)</a></li>
            <li><a href="/index">Главная страница (/index)</a></li>
            <li><a href="/lab1/web">Web-сервер</a></li>
            <li><a href="/lab1/author">Информация об авторе</a></li>
            <li><a href="/lab1/image">Изображение дуба</a></li>
            <li><a href="/lab1/counter">Счетчик посещений</a></li>
            <li><a href="/clear_counter">Очистка счетчика</a></li>
            <li><a href="/test_500">Тест ошибки 500</a></li>
            <li><a href="/test_500_2">Тест ошибки 500 (вариант 2)</a></li>
        </ul>

    </body>
</html>"""

@app.route ("/")
@app.route ("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1> 
               <a href="/author">author</a>
           </body>
        </html>""", 200, {
            "X-Server": "sample", 
            'Content-Type': 'text/plain; charset=utf-8'}

@app.route ("/lab1/author")
def author():
    name = "пенькова полина александровна"
    group = "ФБИ-34"
    faculity = "ФБ"

    return """ <!doctype html>
        <html>
            <body>
                <p>студент: """ + name + """</p>
                <p>группа: """ + group + """</p>
                <p>факультет: """ + faculity + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route ('/lab1/image')
def image():
    image_path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    
    response = '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + image_path + '''">
        <br>
    </body>
</html>'''

    resp = make_response(response)
    
    resp.headers['Content-Language'] = 'ru'
    
    resp.headers['X-Student-Name'] = 'Penkova Polina'
    resp.headers['X-University'] = 'NSTU'
    resp.headers['X-Lab-Number'] = '1'
    
    return resp


count = 0

@app.route('/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect('/counter')

@app.route('/lab1/counter')
def counter():
    global count 
    count += 1 
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        дата и время: ''' + time + '''<br>
        запршенный адрес: ''' + url + '''<br>
        ваш ip-адрес: ''' + client_ip + '''<br>
        <a href="/clear_counter">очистить счетчик</a><br>
    </body>
</html>
'''
@app.route("/lab1/info")
def info():
    return redirect("/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>создано успешно</h1>
        <div><i>что-то создано..</i></div>
    </body>
</html>
''', 201

@app.route('/lab2/a/')
def a():
    return 'со слэшем'

@app.route('/lab2/a')
def a2():
    return 'без слэша'

flower_list = ['подсолнух', 'ромашка', 'мак', 'ландыш', 'ирис']

@app.route('/lab2/add_flower/')
def add_flower_no_name():
    abort(400, description="вы не задали имя цветка")
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>добавлен новый цветок</h1>
    <p>название нового цветка: {name} </p>
    <p>всего цветов: {flower_list}</p>
    </body>
</html>'''

@app.route('/lab2/flowers/')
def show_all_flowers():
    return f'''
<!doctype html>
<html>
    <body>
    <h1>все цветы</h1>
    <p>количество цветов: {len(flower_list)}</p>
    <p>список цветов: {flower_list}</p>
    <a href="/lab2/clear_flowers/">очистить список цветов</a>
    </body>
</html>'''

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return f'''
<!doctype html>
<html>
    <body>
    <h1>информация о цветке</h1>
    <p>цветок: {flower_list[flower_id]}</p>
    <a href="/lab2/flowers/">посмотреть все цветы</a>
    </body>
</html>'''
    
@app.route('/lab2/clear_flowers/')
def clear_flowers():
    flower_list.clear()
    return '''
<!doctype html>
<html>
    <body>
    <h1>список цветов очищен</h1>
    <p>все цветы были удалены из списка.</p>
    <a href="/lab2/flowers/">Перейти к списку всех цветов</a>
    </body>
</html>'''

@app.route('/lab2/example')
def example():
    name  = 'Пенькова Полина'
    lab = 'Лабораторная работа 2'
    group = 'ФБИ-34'
    course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'апельсины', 'price': 120},
        {'name': 'дыни', 'price': 80},
        {'name': 'персики', 'price': 95},
        {'name': 'мандарины', 'price': 321}
    ]
    return render_template('example.html', name=name, lab=lab, group=group, course=course, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    sum_result = a + b
    dif_result = a - b
    mul_result = a * b
    div_result = a / b
    pow_result = a ** b
    return render_template('calc.html', 
                        a=a, 
                        b=b, 
                        sum_result=sum_result,
                        dif_result=dif_result,
                        mul_result=mul_result,
                        div_result=div_result,
                        pow_result=pow_result)


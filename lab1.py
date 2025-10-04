from flask import Blueprint, url_for, request, redirect, make_response
lab1 = Blueprint('lab1', __name__)
import datetime

@lab1.route("/lab1")
def lab():
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

@lab1.route ("/")
@lab1.route ("/lab1/web")
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

@lab1.route ("/lab1/author")
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

@lab1.route ('/lab1/image')
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

@lab1.route('/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect('/counter')

@lab1.route('/lab1/counter')
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
@lab1.route("/lab1/info")
def info():
    return redirect("/author")

@lab1.route("/lab1/created")
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
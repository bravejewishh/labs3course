from flask import Flask, url_for, request, redirect
import datetime
app = Flask (__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы((((", 404

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
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css")
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <h1>дуб</h1>
        <img src="{path}">
    </body>
</html>
'''
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


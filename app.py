from flask import Flask, url_for, request, redirect
import datetime
app = Flask (__name__)

@app.errorhandler(404):
def not_found(err):
    return "нет такой страницы((((", 404

@app.route ("/")
@app.route ("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
               <h1>web-сервер на flask</h1> 
               <a href="/author">author</a>
           </body>
        </html>"""

@app.route ("/author")
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

@app.route ('/image')
def image():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype html>
<html>
    <body>
        <h1>дуб</h1>
        <img src="'''+ path + '''">
    </body>
</html>
'''
count = 0

@app.route('/counter')
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
    </body>
</html>
'''
@app.route("/info")
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


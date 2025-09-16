from flask import Flask
app = Flask (__name__)

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


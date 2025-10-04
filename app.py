from flask import Flask, url_for, request, redirect, make_response, abort, render_template
import datetime
from lab1 import lab1

app = Flask (__name__)
app.register_blueprint(lab1)

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
                <li><a href="/lab2">Вторая лабораторная</a></li>
            </ul>
        </main>
        <footer>
            Пенькова Полина Александровна, ФБИ-34, 3 курс, 2025
        </footer>
    </body>
</html>"""

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


books = [
    {'author': 'Джордж Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
    {'author': 'Джоан Роулинг', 'title': 'Гарри Поттер и философский камень', 'genre': 'Фэнтези', 'pages': 432},
    {'author': 'Джон Р. Р. Толкин', 'title': 'Властелин колец', 'genre': 'Фэнтези', 'pages': 1178},
    {'author': 'Агата Кристи', 'title': 'Убийство в Восточном экспрессе', 'genre': 'Детектив', 'pages': 256},
    {'author': 'Стивен Кинг', 'title': 'Оно', 'genre': 'Ужасы', 'pages': 1248},
    {'author': 'Харпер Ли', 'title': 'Убить пересмешника', 'genre': 'Роман воспитания', 'pages': 416},
    {'author': 'Фрэнсис Скотт Фицджеральд', 'title': 'Великий Гэтсби', 'genre': 'Классика', 'pages': 256},
    {'author': 'Джейн Остин', 'title': 'Гордость и предубеждение', 'genre': 'Любовный роман', 'pages': 480},
    {'author': 'Эрнест Хемингуэй', 'title': 'По ком звонит колокол', 'genre': 'Военная проза', 'pages': 576},
    {'author': 'Габриэль Гарсия Маркес', 'title': 'Сто лет одиночества', 'genre': 'Магический реализм', 'pages': 544},
    {'author': 'Пауло Коэльо', 'title': 'Алхимик', 'genre': 'Притча', 'pages': 256},
    {'author': 'Дэн Браун', 'title': 'Код да Винчи', 'genre': 'Детективный триллер', 'pages': 480},
    {'author': 'Маргарет Митчелл', 'title': 'Унесенные ветром', 'genre': 'Исторический роман', 'pages': 1024},
    {'author': 'Артур Конан Дойл', 'title': 'Приключения Шерлока Холмса', 'genre': 'Детектив', 'pages': 384},
    {'author': 'Оскар Уайльд', 'title': 'Портрет Дориана Грея', 'genre': 'Философский роман', 'pages': 320},
    {'author': 'Рэй Брэдбери', 'title': '451° по Фаренгейту', 'genre': 'Научная фантастика', 'pages': 256},
    {'author': 'Станислав Лем', 'title': 'Солярис', 'genre': 'Научная фантастика', 'pages': 288},
    {'author': 'Умберто Эко', 'title': 'Имя розы', 'genre': 'Исторический детектив', 'pages': 672}
]

@app.route('/lab2/books/')
def show_books():
    return render_template('books.html', books=books)

dogs = [
    {
        'name': 'Лабрадор-ретривер',
        'description': 'Дружелюбная и активная семейная собака',
        'image': 'labrador.jpg'
    },
    {
        'name': 'Немецкая овчарка',
        'description': 'Умная и преданная рабочая порода',
        'image': 'german_shepherd.jpg'
    },
    {
        'name': 'Золотистый ретривер',
        'description': 'Добродушная и терпеливая собака',
        'image': 'golden_retriever.jpg'
    },
    {
        'name': 'Французский бульдог',
        'description': 'Компактная и дружелюбная городская собака',
        'image': 'french_bulldog.jpg'
    },
    {
        'name': 'Бигль',
        'description': 'Энергичная и любопытная гончая',
        'image': 'beagle.jpg'
    },
    {
        'name': 'Пудель',
        'description': 'Умная и элегантная порода',
        'image': 'poodle.jpg'
    },
    {
        'name': 'Ротвейлер',
        'description': 'Сильная и уверенная в себе собака',
        'image': 'rottweiler.jpg'
    },
    {
        'name': 'Йоркширский терьер',
        'description': 'Маленькая собака с большим характером',
        'image': 'yorkie.jpg'
    },
    {
        'name': 'Боксёр',
        'description': 'Энергичная и игривая порода',
        'image': 'boxer.jpg'
    },
    {
        'name': 'Такса',
        'description': 'Смелая и любопытная собака',
        'image': 'dachshund.jpg'
    },
    {
        'name': 'Сибирский хаски',
        'description': 'Энергичная ездовая собака',
        'image': 'husky.jpg'
    },
    {
        'name': 'Доберман',
        'description': 'Элегантная и умная порода',
        'image': 'doberman.jpg'
    },
    {
        'name': 'Австралийская овчарка',
        'description': 'Умная и энергичная рабочая собака',
        'image': 'australian_shepherd.jpg'
    },
    {
        'name': 'Ши-тцу',
        'description': 'Нежная и дружелюбная собака-компаньон',
        'image': 'shih_tzu.jpg'
    },
    {
        'name': 'Бернский зенненхунд',
        'description': 'Спокойная и добродушная пастушья собака',
        'image': 'bernese_mountain.jpg'
    },
    {
        'name': 'Померанский шпиц',
        'description': 'Маленькая и пушистая собака',
        'image': 'pomeranian.jpg'
    },
    {
        'name': 'Кавалер кинг чарльз спаниель',
        'description': 'Нежная и ласковая собака',
        'image': 'cavalier.jpg'
    },
    {
        'name': 'Мопс',
        'description': 'Добродушная и компактная собака',
        'image': 'pug.jpg'
    },
    {
        'name': 'Бордер-колли',
        'description': 'Самая умная порода собак',
        'image': 'border_collie.jpg'
    },
    {
        'name': 'Чихуахуа',
        'description': 'Самая маленькая порода собак',
        'image': 'chihuahua.jpg'
    }
]

@app.route('/lab2/dogs/')
def show_dogs():
    return render_template('dogs.html', dogs=dogs)

@app.route('/lab2/index')
def lab2_index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Лабораторная работа 2</title>
    </head>
    <body>
        <nav>
            <a href="/index">Главное меню</a>
        </nav>
        
        <h1>Лабораторная работа 2</h1>
        
        <h2>Все ссылки лабораторной работы:</h2>
        
        <h3>Примеры и тесты:</h3>
        <ul>
            <li><a href="/lab2/a/">Со слэшем</a></li>
            <li><a href="/lab2/a">Без слэша</a></li>
            <li><a href="/lab2/example">Пример с фруктами</a></li>
            <li><a href="/lab2/filters">Фильтры</a></li>
        </ul>
        
        <h3>Цветы:</h3>
        <ul>
            <li><a href="/lab2/add_flower/">Добавить цветок (ошибка 400)</a></li>
            <li><a href="/lab2/add_flower/Роза">Добавить цветок "Роза"</a></li>
            <li><a href="/lab2/flowers/">Показать все цветы</a></li>
            <li><a href="/lab2/flowers/0">Цветок с ID 0</a></li>
            <li><a href="/lab2/clear_flowers/">Очистить список цветов</a></li>
        </ul>
        
        <h3>Калькулятор:</h3>
        <ul>
            <li><a href="/lab2/calc/5">Калькулятор (5/1)</a></li>
            <li><a href="/lab2/calc/10/3">Калькулятор (10/3)</a></li>
        </ul>
        
        <h3>Книги:</h3>
        <ul>
            <li><a href="/lab2/books/">Список книг</a></li>
        </ul>
        
        <h3>Собаки:</h3>
        <ul>
            <li><a href="/lab2/dogs/">Породы собак</a></li>
        </ul>
    </body>
    </html>
    '''

@app.route('/lab2/index')
def lab2_index2():
    return render_template('lab2.html')
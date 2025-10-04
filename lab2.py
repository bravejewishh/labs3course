from flask import Blueprint, url_for, request, redirect, make_response, abort, render_template
lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/a/')
def a():
    return 'со слэшем'

@lab2.route('/lab2/a')
def a2():
    return 'без слэша'

flower_list = ['подсолнух', 'ромашка', 'мак', 'ландыш', 'ирис']

@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    abort(400, description="вы не задали имя цветка")
    
@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.lab2end(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>добавлен новый цветок</h1>
    <p>название нового цветка: {name} </p>
    <p>всего цветов: {flower_list}</p>
    </body>
</html>'''

@lab2.route('/lab2/flowers/')
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

@lab2.route('/lab2/flowers/<int:flower_id>')
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
    
@lab2.route('/lab2/clear_flowers/')
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

@lab2.route('/lab2/example')
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

@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)

@lab2.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
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

@lab2.route('/lab2/books/')
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

@lab2.route('/lab2/dogs/')
def show_dogs():
    return render_template('dogs.html', dogs=dogs)

@lab2.route('/lab2/index')
def lab2_index():
    return render_template('menu.html')
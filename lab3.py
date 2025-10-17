from flask import Blueprint, render_template, request, make_response, redirect
from datetime import datetime
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    if not name:
        name = 'аноним'

    age = request.cookies.get('age')
    if not age:
        age = 'не указан'

    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response (redirect('/lab3/'))
    resp.set_cookie('name', 'Alex')
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'red')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.set_cookie('name_color', 'black')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'заполните это поле'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'заполните это поле'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', '0')
    try:
        price = int(price)
    except ValueError:
        price = 0
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    background = request.args.get('background')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')

    if color or background or font_size or font_family:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if background:
            resp.set_cookie('background', background)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        return resp

    color = request.cookies.get('color', '#000000') 
    background = request.cookies.get('background', '#ffffff')
    font_size = request.cookies.get('font_size', '16')
    font_family = request.cookies.get('font_family', 'Arial, sans-serif')

    return render_template(
        'lab3/settings.html',
        color=color,
        background=background,
        font_size=font_size,
        font_family=font_family
    )


BERTH_LABELS = {
    'bottom': 'Нижняя',
    'top': 'Верхняя',
    'side_top': 'Верхняя боковая',
    'side_bottom': 'Нижняя боковая'
}

@lab3.route('/lab3/ticket_form')
def ticket_form():
    return render_template('lab3/ticket_form.html', data={}, errors={})

@lab3.route('/lab3/ticket')
def ticket():
    errors = {}
    data = {}

    # Получаем все параметры
    name = request.args.get('name', '').strip()
    berth = request.args.get('berth')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    age_str = request.args.get('age', '').strip()
    departure = request.args.get('departure', '').strip()
    destination = request.args.get('destination', '').strip()
    date_str = request.args.get('date', '').strip()
    insurance = request.args.get('insurance') == 'on'

    data = {
        'name': name,
        'berth': berth,
        'bedding': bedding,
        'luggage': luggage,
        'age': age_str,
        'departure': departure,
        'destination': destination,
        'date': date_str,
        'insurance': insurance
    }

    if not name:
        errors['name'] = 'Укажите ФИО'
    if not berth:
        errors['berth'] = 'Выберите полку'
    if not age_str:
        errors['age'] = 'Укажите возраст'
    else:
        try:
            age = int(age_str)
            if age < 1 or age > 120:
                errors['age'] = 'Возраст должен быть от 1 до 120 лет'
            else:
                data['age'] = age
        except ValueError:
            errors['age'] = 'Возраст должен быть числом'

    if not departure:
        errors['departure'] = 'Укажите пункт выезда'
    if not destination:
        errors['destination'] = 'Укажите пункт назначения'
    if not date_str:
        errors['date'] = 'Укажите дату поездки'
    else:
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            errors['date'] = 'Неверный формат даты'

    if errors:
        return render_template('lab3/ticket_form.html', data=data, errors=errors)

    is_child = age < 18
    base_price = 700 if is_child else 1000
    price = base_price

    if berth in ['bottom', 'side_bottom']:
        price += 100
    if bedding:
        price += 75
    if luggage:
        price += 250
    if insurance:
        price += 150

    return render_template(
        'lab3/ticket.html',
        name=name,
        age=age,
        departure=departure,
        destination=destination,
        date=date_str,
        berth=berth,
        bedding=bedding,
        luggage=luggage,
        insurance=insurance,
        is_child=is_child,
        price=price,
        berth_labels=BERTH_LABELS
    )
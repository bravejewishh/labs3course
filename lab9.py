from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
import random 

lab9 = Blueprint('lab9', __name__, template_folder='templates')

opened_boxes = {}

gifts = [
    {"message": "С Новым годом! 🎄", "image": "/static/lab9/gift1.jpg"},
    {"message": "Пусть сбудутся все мечты! ✨", "image": "/static/lab9/gift2.jpg"},
    {"message": "Здоровья, счастья и удачи! 🍀", "image": "/static/lab9/gift3.png"},
    {"message": "Пусть в доме будет тепло и уют! 🕯️", "image": "/static/lab9/gift4.jpg"},
    {"message": "Желаю успехов в учёбе! 📚", "image": "/static/lab9/gift5.png"},
    {"message": "Пусть рядом будут верные друзья! 👯", "image": "/static/lab9/gift6.png"},
    {"message": "Пусть каждый день приносит радость! ☀️", "image": "/static/lab9/gift7.png"},
    {"message": "Много денег и мало забот! 💰", "image": "/static/lab9/gift8.jpg"},
    {"message": "Пусть любовь согревает сердце! ❤️", "image": "/static/lab9/gift9.jpg"},
    {"message": "Весёлого праздника и вкусных мандаринов! 🍊", "image": "/static/lab9/gift10.jpg"}
]

@lab9.route('/lab9')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(random.randint(100000, 999999))
    return render_template('lab9/index.html')

@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"success": False, "error": "Сессия утеряна"}), 400

    data = request.get_json()
    box_id = data.get('box_id')

    if box_id is None or box_id < 0 or box_id >= len(gifts):
        return jsonify({"success": False, "error": "Неверный номер коробки"}), 400

    # Получаем список открытых коробок для пользователя
    user_opened = opened_boxes.get(user_id, [])
    
    if box_id in user_opened:
        return jsonify({"success": False, "error": "Эта коробка уже открыта!"}), 400

    if len(user_opened) >= 3:
        return jsonify({"success": False, "error": "Вы уже открыли 3 коробки! Больше нельзя."}), 400

    # Открываем коробку
    user_opened.append(box_id)
    opened_boxes[user_id] = user_opened

    gift = gifts[box_id]
    return jsonify({
        "success": True,
        "message": gift["message"],
        "image": gift["image"]
    })
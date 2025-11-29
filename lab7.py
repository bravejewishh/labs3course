from flask import Blueprint, render_template, request, session, redirect, url_for, current_app

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
  {
    "title": "Cowboy Bebop",
    "title_ru": "Ковбой Бибоп",
    "year": 1998,
    "description": "Недалекое будущее, человечество колонизировало Солнечную систему. \
        У преступников есть масса возможностей скрыться от правосудия, поэтому для борьбы \
        с бандитами правительство возродило практику охоты за головами. Спайк и \
        Блэк — наемники, которые летают по космосу на корабле Bebop 268710. \
        По ходу истории экипаж пополняют красотка Фэй, хакер-гений Эд и \
        собака Эйн."
  },
  {
    "title": "Great Teacher Onizuka",
    "title_ru": "Крутой учитель Онидзука",
    "year": 1999,
    "description": "Онидзука Эйкити, известный главарь банды «Онибаку», вместе со своим \
        бывшим одноклассником Рюдзи приезжает в Токио в поисках лучшей жизни. Спокойный и \
        рассудительный Рюдзи открывает собственный автосервис, а Онидзука решает \
        устроиться учителем в школу."
  },
  {
    "title": "Gachiakuta",
    "title_ru": "Гачиакута",
    "year": 2025,
    "description": "Трущобы, в которых живут потомки преступников. Люди за границей трущоб\
        смотрят на их жителей свысока, и считают их людьми второго сорта, брезгливо называя\
        их «местными». Рудо, мальчик-сирота, живёт в трущобах со своим приёмным отцом \
        Легто и зарабатывает на жизнь с помощью своих экстраординарных физических \
        способностей. Но однажды Рудо обвиняют в преступлении, которого он не \
        совершал, и бросают в «бездну», которой боятся даже жители трущоб. \
        Попадая в бездну, Рудо хочет отомстить тем, кто сбросил его в \
        бездну, а именно тем, кто живет на небесах…"
  }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort (404)
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return ({"error": "Film not found"}), 404
    return films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return ({"error": "Film not found"}), 404
    film = request.get_json()
    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    films.append(film)
    new_index = len(films) - 1
    return jsonify({"id": new_index}), 201
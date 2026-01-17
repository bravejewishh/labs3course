function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            const tbody = document.getElementById('film-list-body');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                const tr = document.createElement('tr');

                const tdTitleRus = document.createElement('td');
                const tdTitle = document.createElement('td');
                const tdYear = document.createElement('td');
                const tdActions = document.createElement('td');

                tdTitleRus.textContent = films[i].title_ru;
                if (films[i].title === films[i].title_ru) {
                    tdTitle.textContent = '';
                } else {
                    tdTitle.textContent = films[i].title;
                }
                tdYear.textContent = films[i].year;

                const editBtn = document.createElement('button');
                editBtn.textContent = 'Редактировать';
                editBtn.onclick = function() { editFilm(i); };

                const deleteBtn = document.createElement('button');
                deleteBtn.textContent = 'Удалить';
                deleteBtn.onclick = function() { 
                    deleteFilm(i, films[i].title_ru); 
                };


                tdActions.appendChild(editBtn);
                tdActions.appendChild(deleteBtn);

                tr.appendChild(tdTitleRus);
                tr.appendChild(tdTitle);
                tr.appendChild(tdYear);
                tr.appendChild(tdActions);

                tbody.appendChild(tr);
            }
        });
}

function deleteFilm(id, title_ru) {
    if (!confirm(`Вы действительно хотите удалить фильм "${title_ru}"?`)) {
        return; // пользователь отменил
    }

    fetch(`/lab7/rest-api/films/${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.status === 204) {
            // Успешное удаление — перезагружаем таблицу
            fillFilmList();
        } else if (response.status === 404) {
            alert('Фильм не найден (возможно, уже удалён).');
            fillFilmList(); // всё равно обновим список
        } else {
            alert('Ошибка при удалении фильма.');
        }
    })
    .catch(error => {
        console.error('Ошибка сети:', error);
        alert('Не удалось подключиться к серверу.');
    });
}

function showModal() {
    document.getElementById('filmId').value = '';
    document.getElementById('filmTitle').value = '';
    document.getElementById('filmTitleOrig').value = '';
    document.getElementById('filmYear').value = '';
    document.getElementById('filmDescription').value = '';
    document.getElementById('filmModal').style.display = 'block';
}

function hideModal() {
    document.getElementById('filmModal').style.display = 'none';
}

function sendFilm() {
    const film = {
        title: document.getElementById('filmTitleOrig').value,
        title_ru: document.getElementById('filmTitle').value,
        year: parseInt(document.getElementById('filmYear').value),
        description: document.getElementById('filmDescription').value
    };

    const url = '/lab7/rest-api/films/';
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Ошибка при добавлении фильма');
        }
        return response.json();
    })
    .then(() => {
        fillFilmList();
        hideModal();   
    })
    .catch(error => {
        console.error('Ошибка:', error);
        alert('Не удалось добавить фильм');
    });
}
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
                deleteBtn.onclick = function() { deleteFilm(i, films[i].title_ru); };

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
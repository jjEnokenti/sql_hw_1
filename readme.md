# Домашняя работа 1 по sql

## Реализованы запросы:
1. '/movie/<title>' - Поиск по названию
2. '/movie/year_startTOyear_stop' - Поиск в промежутке годов
3. '/rating/<rating>' - Поиск по возрастному рейтингу
4. '/genre/<genre>' - Поиск по жанру

## И две функции поиска без вьюшек:
1. get_movies_by_type_year_genre(movie_type, year, genre) - Находит и отдет фильмы 
отфильтрованные по типуб году и жанру
2. get_actors(actor_1, actor_2) - Находит актеров, которые играли в паре 
с запрашиваемыми актерами более чем 2 раза
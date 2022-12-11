import sqlite3

from flask import Flask, jsonify

DB_PATH = 'netflix.db'

app = Flask(__name__)


def connect_to_db(db_path=DB_PATH):
    """
    Connect to DB, create cursor
    """
    with sqlite3.connect(db_path) as connection:
        return connection.cursor()


def get_value(sql):
    """
    execute data from DB by query
    """
    cursor = connect_to_db().execute(sql)
    return cursor


def search_by_title(title):
    """
    Function search data into DB by title
    """
    query = (
        f"""
        SELECT title,
        country, MAX(release_year) as release_year,
        listed_in, description
        FROM netflix
        WHERE title='{title}'
        """
    )
    # execute data from DB by query
    execute_query = get_value(query).fetchall()[0]
    # Formatted execute result to dict type
    result = {
        'title': execute_query[0],
        'country': execute_query[1],
        'release_year': execute_query[2],
        'genre': execute_query[3],
        'description': execute_query[4]
    }

    return result


def search_by_year_to_year(start_year, stop_year):
    """
    Function search data into DB by distance between start_year-stop_year
    """
    query = (
        f"""
        SELECT title, release_year FROM netflix
        WHERE release_year BETWEEN {start_year} AND {stop_year}
        GROUP BY title, release_year
        LIMIT 100
        """
    )
    # execute data from DB by query
    execute_query = get_value(query)
    # Formatted execute result to list[dict] type
    result = []
    for movie in execute_query:
        result.append({
            'title': movie[0],
            'release_year': movie[1]
        })

    return result


def search_by_rating(rating):
    """
    Function search data into DB by rating
    """

    # available rating
    dct_ratings = {
        "family": ('G', 'PG', 'PG-13'),
        "adult": ('R', 'NC-17'),
        "children": ('G', 'G'),
    }

    query = (
        f"""
        select title, rating, description
        from netflix
        where rating in {dct_ratings.get(rating, ('TV-MA', 'R'))}
        """
    )
    # execute data from DB by query
    execute_query = get_value(query)
    # Formatted execute result to list[dict] type
    result = []
    for movie in execute_query:
        result.append({
            'title': movie[0],
            'rating': movie[1],
            'description': movie[2]
        })

    return result


def get_actors(actor_1, actor_2):
    """
    Function search actors playing more than 2 time with actor_1 and actor_2
    """
    query = (
        f"""
        SELECT `cast` FROM netflix
        WHERE `cast` LIKE '%{actor_1}%' AND `cast` LIKE '%{actor_2}%'
        GROUP BY `cast`
        """
    )
    # execute data from DB by query
    execute_query = get_value(query)

    # actors dictionary playing with queried actors
    temp = {}

    for actors in execute_query:
        # convert tuple to list for correct create temp dictionary
        actors = set(actors[0].split(', ')) - {actor_1, actor_2}
        # create and increment elements to temp dictionary
        for actor in actors:
            temp[actor] = temp.setdefault(actor, 0) + 1

    # result list with actors playing more than 2 time
    result = [actor for actor, count in temp.items() if count > 2]

    return result


def get_ten_movie_by_genre(genre):
    """
    Function search movie by listed_in
    """
    query = (
        f"""
        SELECT title, description FROM netflix
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY release_year LIMIT 10
        """
    )
    # execute data from DB by query
    execute_query = get_value(query)
    # Formatted execute result to list[dict] type
    result = []
    for movie in execute_query:
        result.append({
            'title': movie[0],
            'description': movie[1]
        })

    return result


def get_movies_by_type_year_genre(movie_type, year, genre):
    """
    Function search movie by type and year and listed_in
    """
    query = (
        f"""
        SELECT title, description
        FROM netflix
        WHERE type='{movie_type}' AND release_year={year} AND listed_in like '%{genre}%'
        """
    )
    # execute data from DB by query
    execute_query = get_value(query)
    # Formatted execute result to list[dict] type
    result = []
    for movie in execute_query:
        result.append({
            'title': movie[0],
            'description': movie[1]
        })

    return result


@app.route('/movie/<title>')
def search_title(title):
    """
    View search by title
    """
    # search by title
    result = search_by_title(title)

    return jsonify(result)


@app.route('/movie/<int:year_start>to<int:year_stop>')
def search_year_to_year(year_start, year_stop):
    """
    View search by distance between start_year-stop_year
    """
    # result search by distance between start_year-stop_year
    result = search_by_year_to_year(year_start, year_stop)

    return jsonify(result)


@app.route('/rating/<rating>')
def search_rating_view(rating):
    """
    View search by rating
    """
    # result search by rating
    result = search_by_rating(rating)

    return jsonify(result)


@app.route('/genre/<genre>')
def get_by_genre_view(genre):
    """
    View search by listed_in
    """
    # result search by listed_in
    result = get_ten_movie_by_genre(genre)

    return jsonify(result)


if __name__ == '__main__':
    app.run(
        debug=True,
        port=8888
    )

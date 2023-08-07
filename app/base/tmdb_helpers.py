import requests, environ, json

env = environ.Env()
environ.Env.read_env()


def tmdb_get_single_movie(search_term, year):
    bearer = env("BEARER")
    api_key = env("TMDB_API_KEY")

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {bearer}"
    }

    url = f"https://api.themoviedb.org/3/search/movie"  # Add the search term to the query parameters  # Add the search term to the query parameters

    # Parametry zapytania
    params = {
        'query': search_term,
        'year': year
    }
    
    response = requests.get(url, headers=headers, params=params).json()
    first_result = response['results'][0]
    # Wyodrębnienie poszczególnych informacji z pierwszego wyniku


    movie = {
        'backdrop_path' : first_result['backdrop_path'],
        'genre_ids' : first_result['genre_ids'],
        'id' : first_result['id'],
        'title' : first_result['title'],
        'original_title' : first_result['original_title'],
        'overview' : first_result['overview'],
        'popularity' : first_result['popularity'],
        'poster_path' : first_result['poster_path'],
        'release_date' : first_result['release_date'][0:4],
        'vote_average' : first_result['vote_average'],
        'vote_count' : first_result['vote_count'],
    }
    url_2 = f"https://api.themoviedb.org/3/movie/{first_result['id']}/credits?api_key={api_key}"
    response = requests.get(url_2, headers=headers).json()

    cast = sorted(
        [
            {
                'name': person['name'],
                'character': person['character'],
                'popularity': person['popularity'],
                'profile_path': person['profile_path'],
            }
            for person in response['cast']
        ],
        key=lambda x: x['popularity'],
        reverse=True
    )

    # Create the crew list, avoiding repetitions in names
    seen_names = set()
    crew = []
    for person in response['crew']:
        if person['name'] not in seen_names:
            crew.append({
                'name': person['name'],
                'popularity': person['popularity'],
                'profile_path': person['profile_path'],
                'known_for_department': person['known_for_department']
            })
            seen_names.add(person['name'])

    # Sort the crew list by popularity in descending order
    crew = sorted(crew, key=lambda x: x['popularity'], reverse=True)

    return {'movie': movie, 'cast': cast, 'crew': crew}


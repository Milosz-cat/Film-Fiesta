import requests, environ

    # Create the crew list, avoiding repetitions in names
    #TODO Ogarnij cos zeby byy wypisane wsytstkie role i co z rezyserem!!!!!!!!!!
class TMDBClient:
    def __init__(self):
        self.bearer = environ.Env()("BEARER")
        self.api_key = environ.Env()("TMDB_API_KEY")
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.bearer}"
        }

    def search_movies(self, search_term):
        url = "https://api.themoviedb.org/3/search/movie"
        params = {'query': search_term}
        response = requests.get(url, headers=self.headers, params=params).json()
        return response['results']
    
    def search_movie(self, search_term, year):
        url = "https://api.themoviedb.org/3/search/movie"
        params = {'query': search_term, 'year': year}
        response = requests.get(url, headers=self.headers, params=params).json()
        return response['results'][0]

    def get_movie_details(self, movie_id):
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def process_cast(self, cast_data):
        return [
            {
                'id': person['id'],
                'name': person['name'],
                'character': person['character'],
                'popularity': person['popularity'],
                'profile_path': person['profile_path'],
                
            }
            for person in cast_data
        ]

    def process_crew(self, crew_data):
        seen_names = set()
        crew = []
        for person in crew_data:
            if person['name'] not in seen_names:
                crew.append({
                    'id': person['id'],
                    'name': person['name'],
                    'popularity': person['popularity'],
                    'profile_path': person['profile_path'],
                    'known_for_department': person['known_for_department']
                })
                seen_names.add(person['name'])
        return sorted(crew, key=lambda x: x['popularity'], reverse=True)

    def get_single_movie(self, search_term, year):
        movie_result = self.search_movie(search_term, year)
        movie_details = self.get_movie_details(movie_result['id'])
        
        movie = {
            'id': movie_result['id'],
            'title': movie_result['title'],
            'poster_path': movie_result['poster_path'],
            'release_date': movie_result['release_date'][0:4],
            'backdrop_path': movie_result['backdrop_path'],
            'vote_average': movie_result['vote_average'],
            'overview': movie_result['overview'],
        }

        cast = self.process_cast(movie_details['cast'])
        crew = self.process_crew(movie_details['crew'])

        return {'movie': movie, 'cast': cast, 'crew': crew}

    def get_single_movie_core(self, search_term, year):
        movie_result = self.search_movie(search_term, year)
        movie = {
            'id': movie_result['id'],
            'title': movie_result['title'],
            'poster_path': movie_result['poster_path'],
            'release_date': movie_result['release_date'][0:4],
        }
        return movie

    def search_person(self, name):
        url = f"https://api.themoviedb.org/3/search/person?api_key={self.api_key}&query={name}"
        response = requests.get(url, headers=self.headers).json()
        return response['results']
    
    def get_movies_by_person(self, person_id):
        url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers).json()
        return response['cast'], response['crew']
    
    def get_movies_by_name(self, name):
        person_results = self.search_person(name)
        if person_results:
            person_id = person_results[0]['id']
            cast_movies, crew_movies = self.get_movies_by_person(person_id)
            return {'actor_movies': cast_movies, 'director_movies': [movie for movie in crew_movies if movie['job'] == 'Director']}
        return {'actor_movies': [], 'director_movies': []}

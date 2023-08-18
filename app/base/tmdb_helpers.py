import requests, environ

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

        # Separate directors and writers from the crew data
        directors = [person for person in movie_details['crew'] if person['job'] == 'Director']
        writers = [person for person in movie_details['crew'] if person['job'] in ['Writer', 'Screenplay', 'Novel']]

        return {'movie': movie, 'cast': cast, 'crew': crew, 'directors': directors , 'writers': writers}

    def get_single_movie_core(self, search_term, year):
        movie_result = self.search_movie(search_term, year)
        print(movie_result)
        movie = {
            'id': movie_result['id'],
            'title': movie_result['title'],
            'poster_path': movie_result['poster_path'],
            'release_date': movie_result['release_date'][0:4],
        }
        return movie
    
    def search_person_by_id(self, person_id):
        url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers).json()
        return response

    def search_person(self, name):
        url = f"https://api.themoviedb.org/3/search/person?api_key={self.api_key}&query={name}"
        response = requests.get(url, headers=self.headers).json()
        return response['results']
    
    def get_movies_by_person(self, person_id):
        url = f"https://api.themoviedb.org/3/person/{person_id}/movie_credits?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers).json()
        cast_movies, crew_movies = response['cast'], response['crew']

        actor_movies = [
            movie for movie in cast_movies
            if 'self' not in movie.get('character', '').lower()
        ]

        director_movies = [
            movie for movie in crew_movies
            if movie['job'] == 'Director' or movie.get('department') == 'Directing'
        ]

        actor_movies = sorted(actor_movies, key=lambda x: x.get('popularity', 0), reverse=True)
        director_movies = sorted(director_movies, key=lambda x: x.get('popularity', 0), reverse=True)
        return actor_movies, director_movies

    def get_trending_movies(self):
        """Retrieve a list of trending movies from TMDb."""
        url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"
        response = requests.get(url, headers=self.headers).json()
        return response['results']
    
    def get_now_playing_movies(self):
        """Retrieve a list of popular movies from TMDb."""
        url = "https://api.themoviedb.org/3/movie/now_playing"
        response = requests.get(url, headers=self.headers).json()
        return response['results']
    
    def get_movie_recommendations(self, movie_id):
        """Retrieve a list of recommended movies for a given movie ID from TMDb."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
        response = requests.get(url, headers=self.headers).json()
        return response['results']

    def get_popular_people(self):
        url = "https://api.themoviedb.org/3/person/popular"
        response = requests.get(url, headers=self.headers).json()
        return response['results']

import requests, environ

class TMDBClient:
    """
    A client for interacting with The Movie Database (TMDb) API.

    This client provides methods to fetch movie, person, and other related data from TMDb.
    It uses the requests library to make HTTP requests and retrieves and process data in JSON format.

    Attributes:
        bearer (str): The bearer token for authentication with the TMDb API.
        api_key (str): The API key for accessing TMDb.
        headers (dict): The headers used in the HTTP requests, including authorization.
    """
    def __init__(self):
        self.bearer = environ.Env()("BEARER")
        self.api_key = environ.Env()("TMDB_API_KEY")
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.bearer}"
        }


    def search_movies(self, search_term):
        """Search for movies based on a given term."""
        url = "https://api.themoviedb.org/3/search/movie"
        params = {'query': search_term}
        response = requests.get(url, headers=self.headers, params=params).json()
        return response['results']
 

    def search_movie(self, search_term, year):
        """Search for a specific movie by its title and release year."""
        url = "https://api.themoviedb.org/3/search/movie"
        params = {'query': search_term, 'year': year}
        response = requests.get(url, headers=self.headers, params=params).json()

        # If no results, try with one more year
        if not response['results']:
            params['year'] = str(int(year) + 1)
            response = requests.get(url, headers=self.headers, params=params).json()

        return response['results'][0]


    def get_movie_persons(self, movie_id):
        """Retrieve cast and crew details for a given movie ID."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers).json()
        return response


    def get_movie_detalis(self, movie_id):
        """Fetch detailed information for a specific movie by its ID."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers).json()
        return response


    def process_cast(self, cast_data):
        """Format and return the provided cast data."""
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
        """Format, sort and return the provided crew data, removing duplicates."""
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


    def format_number(self, number):
        """Convert a number into a human-readable string format."""
        if number >= 1_000_000_000:  # billions
            return f"{number // 1_000_000_000} mld $ "
        elif number >= 1_000_000:  # millions
            return f"{number // 1_000_000} mln $ "
        elif number >= 1_000:  # thousands
            return f"{number // 1_000} k $ "
        else:
            return str(number)


    def get_single_movie(self, search_term, year):
        """
        Retrieve comprehensive details by combining other methods.
        It is directly used for a page about a specific movie.
        """
        movie_result = self.search_movie(search_term, year)
        movie_persons = self.get_movie_persons(movie_result['id'])
        movie_detalis = self.get_movie_detalis(movie_result['id'])

        duration = f"{movie_detalis['runtime'] // 60}h {movie_detalis['runtime'] - (movie_detalis['runtime'] // 60)*60}m"

        movie = {
            'id': movie_result['id'],
            'title': movie_result['title'],
            'poster_path': movie_result['poster_path'],
            'release_date': movie_result['release_date'][0:4],
            'backdrop_path': movie_result['backdrop_path'],
            'vote_average': movie_result['vote_average'],
            'overview': movie_result['overview'],
            'genres': movie_detalis['genres'],
            'budget' : self.format_number(movie_detalis['budget']),
            'revenue' : self.format_number(movie_detalis['revenue']),
            'duration': duration,
        }

        cast = self.process_cast(movie_persons['cast'])
        crew = self.process_crew(movie_persons['crew'])

        # Separate directors and writers from the crew data
        directors = [person for person in movie_persons['crew'] if person['job'] == 'Director']
        writers = [person for person in movie_persons['crew'] if person['job'] in ['Writer', 'Screenplay', 'Novel']]

        return {'movie': movie, 'cast': cast, 'crew': crew, 'directors': directors , 'writers': writers}


    def get_single_movie_core(self, search_term, year):
        """
        Fetch core details (ID, title, poster, release date) of a specific movie.
        It is directly used for rating movie or adding it to list. 
        """
        movie_result = self.search_movie(search_term, year)

        movie = {
            'id': movie_result['id'],
            'title': movie_result['title'],
            'poster_path': movie_result['poster_path'],
            'release_date': movie_result['release_date'][0:4],
        }
        return movie


    def search_person_by_id(self, person_id):
        """Search for a person's details using their unique ID."""
        url = f"https://api.themoviedb.org/3/person/{person_id}?api_key={self.api_key}"
        response = requests.get(url, headers=self.headers).json()
        return response


    def search_person(self, name):
        """Search for a person based on their name."""
        url = f"https://api.themoviedb.org/3/search/person?api_key={self.api_key}&query={name}"
        response = requests.get(url, headers=self.headers).json()
        return response['results']


    def get_movies_by_person(self, person_id):
        """Retrieve movies associated with a specific person, categorized by their role."""
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
        """Retrieve the list of movies that are currently playing in theaters."""
        url = "https://api.themoviedb.org/3/movie/now_playing"
        response = requests.get(url, headers=self.headers).json()
        return response['results']


    def get_movie_recommendations(self, movie_id):
        """Fetch movie recommendations based on a specific movie ID."""
        url = f"https://api.themoviedb.org/3/movie/{movie_id}/recommendations"
        response = requests.get(url, headers=self.headers).json()
        return response['results']



    def get_popular_people(self):
        """Retrieve a list of popular personalities in the movie industry."""
        url = "https://api.themoviedb.org/3/person/popular"
        response = requests.get(url, headers=self.headers).json()
        return response['results']

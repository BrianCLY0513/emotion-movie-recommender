import requests

API_KEY = "3a41a988524c90f7120c22e2df9db9e2"

def fetch_poster(movie_title):

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"

    data = requests.get(url).json()

    if "results" in data and len(data["results"]) > 0:

        poster_path = data["results"][0]["poster_path"]

        if poster_path:   # check if poster exists
            return "https://image.tmdb.org/t/p/w500" + poster_path

    return None
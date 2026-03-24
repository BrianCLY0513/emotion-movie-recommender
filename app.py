import streamlit as st
from recommender import recommend_movies, movies, get_popular_movies, get_movie_details
from poster import fetch_poster

st.set_page_config(page_title="Emotion Movie Recommender", layout="wide")

st.title("🎬 Emotion-Based Movie Recommender")
st.write("Find movies that match your mood!")

# Sidebar
st.sidebar.header("Settings")

emotion = st.sidebar.selectbox(
    "Select your mood",
    ["Happy", "Sad", "Stressed", "Excited", "Romantic"]
)

algorithm = st.sidebar.selectbox(
    "Recommendation Algorithm",
    ["Collaborative Filtering", "Content-Based", "Hybrid"]
)

# ⭐ Search Function
search = st.text_input("🔍 Search movie")

if search:
    filtered_movies = movies[
        movies["title"].str.lower().str.contains(search.lower(), na=False)
    ]

    # ⭐ Show number of results
    st.write(f"{len(filtered_movies)} movies found")

    if len(filtered_movies) > 0:
        movie_title = st.selectbox(
            "Select from search results",
            filtered_movies["title"].values
        )
    else:
        st.warning("No movies found. Try another keyword.")
        movie_title = st.selectbox(
            "Choose a movie you like",
            movies["title"].values
        )
else:
    movie_title = st.selectbox(
        "Choose a movie you like",
        movies["title"].values
    )

    

# ⭐ Emotion explanation
st.write(f"Showing **{emotion}** movies to match your mood 😊")

# ⭐ Popular Movies Section
st.subheader("🔥 Popular Movies")

popular_movies = get_popular_movies()
st.write(popular_movies)

# ⭐ Recommendation Button
if st.button("Recommend Movies"):

    # Select algorithm
    if algorithm == "Collaborative Filtering":
        recommendations = recommend_movies(movie_title, emotion)

    elif algorithm == "Content-Based":
        try:
            recommendations = recommend_movies_cb(movie_title, emotion)
        except:
            st.warning("Content-Based model not implemented yet")
            recommendations = []

    elif algorithm == "Hybrid":
        try:
            recommendations = recommend_movies_hybrid(movie_title, emotion)
        except:
            st.warning("Hybrid model not implemented yet")
            recommendations = []

    st.subheader("Recommended Movies")

    cols = st.columns(5)

    for i, movie in enumerate(recommendations):

        poster = fetch_poster(movie)
        details = get_movie_details(movie)


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("dataset/movies.csv")
ratings = pd.read_csv("dataset/ratings.csv")

# Merge dataset
data = pd.merge(ratings, movies, on="movieId")

# Emotion → Genre mapping
emotion_map = {
    "Happy": ["Comedy", "Animation"],
    "Sad": ["Drama"],
    "Stressed": ["Comedy"],
    "Excited": ["Action"],
    "Romantic": ["Romance"]
}

# Create user-movie matrix
user_movie_matrix = data.pivot_table(
    index="userId",
    columns="title",
    values="rating"
)

user_movie_matrix = user_movie_matrix.fillna(0)

# Train model using cosine similarity
movie_similarity = cosine_similarity(user_movie_matrix.T)

# Convert similarity into dataframe
movie_similarity_df = pd.DataFrame(
    movie_similarity,
    index=user_movie_matrix.columns,
    columns=user_movie_matrix.columns
)

# # Calculate similarity
# similarity = cosine_similarity(user_movie_matrix)

def recommend_movies(movie_title, emotion):

    if movie_title not in movie_similarity_df.columns:
        return []

    similar_scores = movie_similarity_df[movie_title].sort_values(ascending=False)

    similar_scores = similar_scores.drop(movie_title, errors='ignore')

    genres = emotion_map.get(emotion, [])

    recommended = []
    fallback = []   # store similar movies without emotion filter

    for movie in similar_scores.index:

        movie_genres = movies[movies["title"] == movie]["genres"].values

        if len(movie_genres) > 0:

            # Check emotion match
            if any(g in movie_genres[0] for g in genres):
                recommended.append(movie)
            else:
                fallback.append(movie)

        # Stop early if enough
        if len(recommended) >= 10:
            break

    # ⭐ If not enough emotion-matching movies → fill with similar movies
    if len(recommended) < 10:
        for movie in fallback:
            if movie not in recommended:
                recommended.append(movie)
            if len(recommended) >= 10:
                break

    return recommended

# Get top popular movies (based on average rating)
def get_popular_movies():
    popular = data.groupby("title")["rating"].mean().sort_values(ascending=False).head(10)
    return popular

# Get movie details (genre + rating)
def get_movie_details(movie):
    movie_info = movies[movies["title"] == movie]

    avg_rating = data[data["title"] == movie]["rating"].mean()

    return {
        "genres": movie_info["genres"].values[0].replace("|", ", ")
        if len(movie_info) > 0 else "N/A",
        "rating": round(avg_rating, 2) if avg_rating else "N/A"
    }

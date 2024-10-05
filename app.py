'''
Project Name: Movie Recommendation System
Author: Syed Shayan Shahid
Email: shayansynshahid@gmail.com
Batch: PGD Batch 6 Data Science with Articficial Intelligence
'''

import os
import pickle
import streamlit as st
import requests
import gzip

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d94a462aa6a6068591ba7b85b7eca533"
    data = requests.get(url)
    data = data.json()
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None
    
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        poster = fetch_poster(movie_id)
        if poster:
            recommended_movie_posters.append(poster)
        else:
            recommended_movie_posters.append("https://via.placeholder.com/500x750?text=No+Image")
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

st.header('🎬 Movie Recommender System Using Machine Learning 🍿')

file_path = os.path.join('artifacts', 'movies.pkl')

try:
    with gzip.open(file_path, 'rb') as f:
        movies = pickle.load(f)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' does not exist.")

with gzip.open('artifacts/movies.pkl', 'rb') as f:
    movies = pickle.load(f)

with gzip.open('artifacts/similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

movie_titles = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_titles
)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

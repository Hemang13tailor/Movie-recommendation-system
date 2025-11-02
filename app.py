import streamlit as st
import pickle
import requests
import pandas as pd
import time
import random

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")

API_KEY = "f156e67c15869dcf0adaed1a88b3a56c"

def get_movie_info(movie_id):
    """Fetch and cache all movie info: details + cast + poster"""
    base_url = "https://api.themoviedb.org/3/movie"
    urls = {
        "details": f"{base_url}/{movie_id}?api_key={API_KEY}&language=en-US",
        "credits": f"{base_url}/{movie_id}/credits?api_key={API_KEY}&language=en-US"
    }

    def safe_request(url):
        for attempt in range(3):  # up to 3 retries
            try:
                res = requests.get(url, timeout=10)
                res.raise_for_status()
                return res.json()
            except Exception as e:
                print(f"Retry {attempt+1} failed for {url}: {e}")
                time.sleep(random.uniform(0.5, 1.5))
        return {}

    details = safe_request(urls["details"])
    credits = safe_request(urls["credits"])

    poster = (
        "https://image.tmdb.org/t/p/w500" + details.get("poster_path", "")
        if details.get("poster_path")
        else "https://via.placeholder.com/500x750?text=No+Image"
    )
    cast = ", ".join([c["name"] for c in credits.get("cast", [])[:5]]) or "Cast info unavailable"

    return {
        "title": details.get("title", "N/A"),
        "overview": details.get("overview", "No overview available."),
        "release_date": details.get("release_date", "N/A"),
        "rating": details.get("vote_average", "N/A"),
        "poster": poster,
        "cast": cast,
        "id": movie_id
    }

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        info = get_movie_info(movie_id)
        recommended_movies.append(info)
    return recommended_movies

st.title("🎬 Movie Recommendation System")
st.markdown("##### Find movies similar to your favorite ones, with live TMDb data!")

# Autocomplete Search Bar
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🔍 Type or select a movie:",
    movie_list,
    index=None,
    placeholder="Search for a movie..."
)

if selected_movie:
    if st.button("Recommend 🎥"):
        with st.spinner("Fetching recommendations..."):
            recommendations = recommend(selected_movie)

        st.subheader(f"Because you liked **{selected_movie}**, you might enjoy:")
        cols = st.columns(5)

        for i, rec in enumerate(recommendations):
            with cols[i]:
                st.image(rec['poster'], use_container_width=True)
                st.markdown(f"**{rec['title']}**")
                with st.expander("ℹ️ More info"):
                    st.markdown(f"**Release Date:** {rec['release_date']}")
                    st.markdown(f"**Rating:** ⭐ {rec['rating']}")
                    st.markdown(f"**Cast:** {rec['cast']}")
                    st.markdown(f"**Overview:** {rec['overview']}")
    

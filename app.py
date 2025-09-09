import streamlit as st
import pickle
import requests
import pandas as pd

# --- Helper Functions ---

def fetch_poster(movie_id):
    """Fetches a movie poster from the TMDb API."""
    # IMPORTANT: Replace YOUR_API_KEY with the key you got from TMDb
    api_key = "f156e67c15869dcf0adaed1a88b3a56c" # Use your actual key here
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            # Return a placeholder if no poster is found
            return "https://via.placeholder.com/500x750.png?text=No+Poster"
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "https://via.placeholder.com/500x750.png?text=API+Error"

def recommend(movie_title):
    """Recommends movies based on the selected movie."""
    try:
        # Find the index of the movie
        movie_index = movies_df[movies_df['title'] == movie_title].index[0]
    except IndexError:
        st.error("Movie not found in the dataset.")
        return [], []
        
    # Get similarity scores and sort them
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6] # Top 5
    
    recommended_movies_names = []
    recommended_movies_posters = []
    
    for i in movies_list:
        movie_id = movies_df.iloc[i[0]].id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_names.append(movies_df.iloc[i[0]].title)
        
    return recommended_movies_names, recommended_movies_posters


# --- Load Pre-computed Data ---
# Load the movie list and similarity matrix we saved in Stage 1
try:
    movies_df = pd.DataFrame(pickle.load(open('movies_list.pkl', 'rb')))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please run the model_builder.py script first.")
    st.stop()


# --- Streamlit User Interface ---

st.set_page_config(layout="wide")
st.title('🎬 Movie Recommendation System')
st.markdown("Select a movie you like, and we'll suggest 5 similar ones!")

selected_movie_name = st.selectbox(
    'Choose a movie from the dropdown:',
    movies_df['title'].values
)

if st.button('Recommend'):
    with st.spinner('Finding recommendations...'):
        names, posters = recommend(selected_movie_name)
    
    if names:
        st.subheader("Here are your recommendations:")
        # Create 5 columns to display the movies
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(names[i])
                st.image(posters[i])
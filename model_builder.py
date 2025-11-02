import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

df = pd.read_csv('cleaned_movies_metadata.csv')
print("Data loaded:", df.shape)
print(df.head(3))

tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=5000
)

tfidf_matrix = tfidf.fit_transform(df['metadata'])
print("TF-IDF matrix shape:", tfidf_matrix.shape)

similarity = cosine_similarity(tfidf_matrix)
print("Cosine similarity matrix computed:", similarity.shape)

def recommend(movie_title, df=df, similarity=similarity):
    """
    Given a movie title, recommend top 5 similar movies.
    """
    if movie_title not in df['title'].values:
        print(f"'{movie_title}' not found in database.")
        return []

    # Get index of the movie
    idx = df[df['title'] == movie_title].index[0]

    # Retrieve pairwise similarity scores
    distances = list(enumerate(similarity[idx]))

    # Sort by similarity (descending) and take top 5 (excluding itself)
    top_matches = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = [df.iloc[i[0]].title for i in top_matches]
    print(f"\n Because you liked '{movie_title}', you may also like:")
    for m in recommended_movies:
        print("   →", m)
    return recommended_movies

# Quick test
recommend('Avatar')

# Save model artifacts for app deployment
pickle.dump(df, open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
print("\n Pickle files saved: movies.pkl and similarity.pkl")

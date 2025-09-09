import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# 1. Load your dataset (e.g., the one from Kaggle's TMDB 5000 movies)
df = pd.read_csv('tmdb_5000_movies.csv')
# For simplicity, let's just use the overview for recommendations
df = df[['id', 'title', 'overview']]
df.dropna(inplace=True)

# 2. Vectorize the 'overview' text data
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['overview'])

# 3. Compute the Cosine Similarity Matrix
similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

# 4. Save the processed dataframe and the similarity matrix to disk
# This is the crucial step for your web app
pickle.dump(df.to_dict(orient='records'), open('movies_list.pkl', 'wb'))
pickle.dump(similarity_matrix, open('similarity.pkl', 'wb'))

print("Model and data saved successfully!")
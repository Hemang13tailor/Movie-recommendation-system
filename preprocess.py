import pandas as pd
import numpy as np
import ast
from collections import Counter
import matplotlib.pyplot as plt


df = pd.read_csv('tmdb_5000_movies.csv')
print(df.shape)
print(df.columns.tolist())

print(df.info())
print(df.isna().sum())

print(df.head(5))

print(df[['title', 'genres', 'keywords', 'overview']].head(3))

def extract_names(obj):
    """Extract 'name' field from JSON-like string column"""
    try:
        items = ast.literal_eval(obj)
        return [d['name'] for d in items]
    except:
        return []

def get_director(obj):
    """Extract director name from crew JSON"""
    try:
        items = ast.literal_eval(obj)
        for d in items:
            if d.get('job') == 'Director':
                return d['name']
        return np.nan
    except Exception:
        return np.nan

def get_top_cast(obj, top_n=3):
    """Extract top N cast names"""
    try:
        items = ast.literal_eval(obj)
        names = [d['name'] for d in items[:top_n]]
        return names
    except Exception:
        return []

def clean_list_text(lst):
    """Convert list of strings to a single lowercase space-free string"""
    return ' '.join(i.replace(" ", "").lower() for i in lst)


df['genres'] = df['genres'].apply(extract_names)
df['keywords'] = df['keywords'].apply(extract_names)

for col in ['genres', 'keywords']:
    if col in df.columns:
        df[col] = df[col].apply(clean_list_text)

df['overview'] = df['overview'].fillna("")
combine_cols = ['overview', 'genres', 'keywords']

df['metadata'] = df[combine_cols].apply(lambda x: ' '.join(x.values.astype(str)), axis=1)

print("\nMetadata column created successfully!")
print(df[['title', 'metadata']].head(3))

all_genres = []
for g in df['genres']:
    all_genres.extend(g.split())
genre_counts = Counter(all_genres)
top_genres = genre_counts.most_common(10)

plt.figure(figsize=(8, 4))
plt.barh([g for g, _ in top_genres], [c for _, c in top_genres])
plt.title("Top 10 Movie Genres")
plt.xlabel("Count")
plt.show()

# Missing overview check
missing_overview = df['overview'].isna().sum()
print(f"\nMovies missing overview: {missing_overview}")

# Sample movie metadata preview 
print("\nExample movie metadata:\n")
for i in range(3):
    print(f" {df.loc[i, 'title']}")
    print(df.loc[i, 'metadata'][:200], '...\n')

# Save cleaned data for next phase
df[['id', 'title', 'metadata']].to_csv("cleaned_movies_metadata.csv", index=False)
print(" Cleaned metadata saved to 'cleaned_movies_metadata.csv'")

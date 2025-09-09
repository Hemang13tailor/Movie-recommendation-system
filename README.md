🎬 Movie Recommendation System

A content-based movie recommender system built with Python and Scikit-learn, deployed as an interactive web application using Streamlit. The app recommends movies based on their plot similarity and fetches live data from the TMDb API.(Note: You should replace this with a screenshot of your own running application!)🌟 OverviewThis project presents a content-based recommendation engine that suggests movies to users based on their similarity to a movie they like. The core of the system is built on Natural Language Processing (NLP) techniques to analyze and compare movie plots. The entire pipeline, from data processing to a user-facing web app, is designed to be efficient and scalable.✨ FeaturesContent-Based Recommendations: Suggests movies based on plot summary similarity using TF-IDF and Cosine Similarity.Interactive UI: A user-friendly web interface built with Streamlit allows users to easily select a movie and get recommendations.Dynamic Data Fetching: Integrates with The Movie Database (TMDb) API to fetch real-time movie details, including posters and overviews.Efficient Pipeline: A two-stage pipeline separates heavy-duty model computation from the lightweight live application, ensuring a fast and responsive user experience.🛠️ Technology StackBackend: PythonData Manipulation: Pandas, NumPyMachine Learning: Scikit-learnWeb Framework: StreamlitAPI: TMDb REST APISerialization: Pickle⚙️ Project ArchitectureThe project is built on an efficient two-stage pipeline:Offline Pre-computation (model_builder.py):Loads the movie dataset.Cleans and preprocesses the text data (plot overviews).Uses TF-IDF to vectorize the text into a numerical matrix.Computes a pairwise cosine similarity matrix for all movies.Saves the processed data and the similarity matrix as pickle files (movies_list.pkl, similarity.pkl).Live Web Application (app.py):Loads the pre-computed data and similarity matrix.Renders a user interface using Streamlit.Takes user input (a selected movie).Looks up the similarity scores for the selected movie.Fetches posters and details for the top N recommended movies from the TMDb API.Displays the recommendations to the user in real-time.This architecture ensures that the computationally expensive tasks are performed only once, allowing the web app to be fast and lightweight.🚀 How to Run This Project LocallyFollow these steps to set up and run the project on your own machine.1. PrerequisitesPython 3.7+An API key from The Movie Database (TMDb).2. Clone the Repositorygit clone [https://github.com/YOUR_USERNAME/movie-recommendation-system.git](https://github.com/YOUR_USERNAME/movie-recommendation-system.git)
cd movie-recommendation-system
3. Set Up a Virtual EnvironmentIt's recommended to use a virtual environment to manage dependencies.# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
4. Install DependenciesCreate a requirements.txt file with the following content:streamlit
pandas
numpy
scikit-learn
requests
Then, install the required libraries:pip install -r requirements.txt
5. Get the DatasetDownload the "TMDB 5000 Movie Dataset" from Kaggle. Place the tmdb_5000_movies.csv file in the root directory of the project.6. Run the Pre-computation ScriptFirst, you need to generate the model files.python model_builder.py
This will create movies_list.pkl and similarity.pkl.7. Run the Streamlit AppBefore running, make sure to add your TMDb API key in the app.py file:# In app.py, find this line and replace the placeholder
api_key = "YOUR_TMDB_API_KEY_HERE"
Now, launch the application:streamlit run app.py
Your web browser should open with the app running at http://localhost:8501.🔮 Future EnhancementsHybrid Recommendation Model: Combine the current content-based approach with collaborative filtering (user-item ratings) for more personalized and diverse recommendations.Improved Feature Engineering: Incorporate more features like genres, cast, director, and keywords into the similarity calculation.User Accounts: Add functionality for user registration, watchlists, and movie ratings.Advanced Search: Replace the dropdown with a live search bar.📄 LicenseThis project is licensed under the MIT License. See the LICENSE file for details.

import streamlit as st
import difflib
import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv(r'/Users/anandanr/Docs/Code/ML/Project/movies.csv')  # Update with your file path

# Placeholder for the similarity matrix (load or calculate it)
# Example: similarity = np.load('similarity_matrix.npy') or replace with your similarity matrix
similarity = np.random.rand(len(df), len(df))  # Replace this with your actual similarity matrix

# Define the recommendation function
def recommend_movies(movie_name, df, similarity):
    # List of all titles
    list_of_all_titles = df['title'].tolist()

    # Find close matches
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles, cutoff=0.3)
    if not find_close_match:
        return None, "No close match found for the movie name."

    close_match = find_close_match[0]
    index_of_the_movie = df[df.title == close_match]['index'].values[0]

    # Ensure the index is within bounds for the similarity matrix
    if index_of_the_movie >= len(similarity):
        return None, "Movie index is out of range for the similarity matrix."

    # Calculate similarity scores
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)

    # Get top movie recommendations
    recommended_movies = []
    for i, movie in enumerate(sorted_similar_movies[:30], start=1):
        index = movie[0]
        title_from_index = df[df.index == index]['title'].values[0]
        recommended_movies.append((i, title_from_index))

    return recommended_movies, None

# Streamlit UI
st.title("Movie Recommendation System")
st.subheader("Find movies similar to your favorite one!")

# User input
movie_name = st.text_input("Enter your favorite movie name:")

# Button to trigger recommendations
if st.button("Find Recommendations"):
    if movie_name:
        # Get recommendations
        recommendations, error = recommend_movies(movie_name, df, similarity)
        
        if error:
            st.write(error)
        elif recommendations:
            st.write(f"Movies suggested for you based on '{movie_name}':")
            for i, title in recommendations:
                st.write(f"{i}. {title}")
        else:
            st.write("No recommendations found.")
    else:
        st.write("Please enter a movie name to get recommendations.")
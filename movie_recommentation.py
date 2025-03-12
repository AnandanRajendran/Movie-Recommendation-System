import streamlit as st
import difflib
import pandas as pd
import numpy as np


df = pd.read_csv(r'/Users/anandanr/Docs/Code/ML/Project/movies.csv')  
similarity = np.random.rand(len(df), len(df))  


def recommend_movies(movie_name, df, similarity):

    list_of_all_titles = df['title'].tolist()


    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles, cutoff=0.3)
    if not find_close_match:
        return None, "No close match found for the movie name."

    close_match = find_close_match[0]
    index_of_the_movie = df[df.title == close_match]['index'].values[0]


    if index_of_the_movie >= len(similarity):
        return None, "Movie index is out of range for the similarity matrix."


    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)


    recommended_movies = []
    for i, movie in enumerate(sorted_similar_movies[:30], start=1):
        index = movie[0]
        title_from_index = df[df.index == index]['title'].values[0]
        recommended_movies.append((i, title_from_index))

    return recommended_movies, None


st.title("Movie Recommendation System")
st.subheader("Find movies similar to your favorite one!")


movie_name = st.text_input("Enter your favorite movie name:")


if st.button("Find Recommendations"):
    if movie_name:

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

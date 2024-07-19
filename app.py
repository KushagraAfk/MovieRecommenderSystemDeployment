import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    path = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f9b81fbce795a5788958d033249606c0&language=en-US'.format(movie_id))
    return "https://image.tmdb.org/t/p/w500" + path.json()["poster_path"]


movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = pd.DataFrame(movies_list)
similarity1 = pickle.load(open('similarity1.pkl', 'rb'))
similarity2 = pickle.load(open('similarity2.pkl', 'rb'))
similarity3 = pickle.load(open('similarity3.pkl', 'rb'))
similarity4 = pickle.load(open('similarity4.pkl', 'rb'))
similarity5 = pickle.load(open('similarity5.pkl', 'rb'))
similarity6 = pickle.load(open('similarity6.pkl', 'rb'))
similarity7 = pickle.load(open('similarity7.pkl', 'rb'))
similarity8 = pickle.load(open('similarity8.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox("What movie did you just watch?", movies_list['title'].values)


def get_similarity(index):
    if index//600 == 0:
        return similarity1
    elif index//600 == 1:
        return similarity2
    elif index//600 == 2:
        return similarity3
    elif index//600 == 3:
        return similarity4
    elif index//600 == 4:
        return similarity5
    elif index//600 == 5:
        return similarity6
    elif index//600 == 6:
        return similarity7
    else:
        return similarity8


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    sim = get_similarity(movie_index)
    movie_index = movie_index % 600 
    movie_list = sorted(list(enumerate(sim[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    movie_names = []
    movie_posters = []

    for a in movie_list:
        movie_names.append(movies_list.iloc[a[0]].title)
        movie_posters.append(fetch_poster(movies_list.iloc[a[0]].id))
    return movie_names, movie_posters


if st.button("Recommend"):
    st.subheader(":blue[Here are some recommendations based on the movie:] ")
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.subheader(names[0])

    with col2:
        st.image(posters[1])
        st.subheader(names[1])

    with col3:
        st.image(posters[2])
        st.subheader(names[2])

    with col4:
        st.image(posters[3])
        st.subheader(names[3])

    with col5:
        st.image(posters[4])
        st.subheader(names[4])


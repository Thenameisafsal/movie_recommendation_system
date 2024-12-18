import streamlit as st
import pickle
import requests

movies = pickle.load(open("movies.pkl","rb"))
similarity = pickle.load(open("similarity.pkl","rb"))
movies_list = movies["title"].values
st.header("Movie Recommender System")
selected_movie = st.selectbox("select movie from dropdown",movies_list) 


def get_posters(movie_id):
#   9ac78a663cc90fe222bc9cdbfb07be11 - api key
    url = "https://api.themoviedb.org/3/movie/{}?api_key=9ac78a663cc90fe222bc9cdbfb07be11&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path

def recommend(movie): # so this will do the recommendation of the top 5 movies, can be leveraged based on the needs
  index = movies[movies["title"] == movie].index[0]
  similarity_values = sorted(list(enumerate(similarity[index])),reverse=True, key = lambda x:x[1])
  recommended_movies = []
  posters = []
  for value in similarity_values[:5]:
    movie_id = movies.iloc[value[0]].id
    recommended_movies.append(movies.iloc[value[0]].title)
    posters.append(get_posters(movie_id))
  return recommended_movies, posters    
if st.button("show recommendations"):
  recom_movies, posters = recommend(selected_movie)
  c1, c2, c3, c4, c5 = st.columns(5)
  with c1:
    st.text(recom_movies[0])
    st.image(posters[0])
  with c2:
    st.text(recom_movies[1])
    st.image(posters[1])
  with c3:
    st.text(recom_movies[2])
    st.image(posters[2])
  with c4:
    st.text(recom_movies[3])
    st.image(posters[3])
  with c5:
    st.text(recom_movies[4])
    st.image(posters[4])


from streamlit_option_menu import option_menu
import streamlit as st
import pickle
import http.client
import json
from urllib.parse import quote
import requests
import numpy as np
import tracemalloc

# Start tracing memory allocations
tracemalloc.start()

@st.cache_resource()
def load_model():
    similarities = []
    for i in range(15): #D:\PROJECTS\Movie-recommender-system\streamlitWebApp\similarity_chunk_1.pkl
        filename = f"similarity_chunk_{i+1}.pkl"
    # streamlitWebApp\similarity_chunk_1.pkl
        with open(filename, 'rb') as f:
            chunk_data = pickle.load(f)
            similarities.append(chunk_data)

    # Concatenate all chunks into a single similarity matrix
    similarity = np.concatenate(similarities, axis=0)

    return similarity


similarity = load_model()
movies_list = pickle.load(open('movies.pkl', 'rb'))  # Keep the original DataFrame

@st.cache_data()
def GetMovieFromID(id):
    url = f"https://api.themoviedb.org/3/movie/{id}?language=en-US"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMDg0YjA1ZDhhMzM1MTJjYWQwYTI3ZDM1MmZiYTljNCIsInN1YiI6IjY1YmY2ODRjYTM1YzhlMDE2M2Q1NTk5OCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.obJ65ZxM_vuIPmjQPZQ4j8bkJSLF4qKQEzdK3VV80ng"
    }

    response = requests.get(url, headers=headers)

    if response.ok:
        return response.json()
    else:
        return None

@st.cache_data()
def GetMovieFromName(movie_name):
    # print("Movie name in getMovieFromName: ", movie_name)
    # API key for the collectapi.com
    myAPI_key = "apikey 4TpzMkeibWYoLfCtFlnwKI:3mSnUaq2ZbUc7JicmqQ8W1"

    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': myAPI_key
    }

    encoded_movie_name = quote(movie_name)
    conn.request("GET", f"/imdb/imdbSearchByName?query={encoded_movie_name}", headers=headers)

    res = conn.getresponse()    
    data = res.read()
    decoded_data = data.decode("utf-8")

    json_data = json.loads(decoded_data)
    # print("Movie json data in getMovieFromName: ", json_data)
    if 'result' in json_data:
        movies = json_data['result']

        if movies:
            return movies[0]

@st.cache_data()
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    fetched_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommend_movies = []
    posters = []

    for j in fetched_movies[1:6]:
        movieDataFetched = GetMovieFromName(movies_list.iloc[j[0]].title)
        if movieDataFetched and 'Poster' in movieDataFetched:
            posters.append(movieDataFetched['Poster'])
            recommend_movies.append(movies_list.iloc[j[0]].title)

    return posters, recommend_movies


def main():
    st.subheader(":movie_camera: WATCH NOW")
    # A random movie extracted from the dataset
    # and its details and posters fetched from imdb website using the imdb API

    col6, col7, col8 = st.columns(3)

    all_movie_titles = movies_list['title'].tolist()

    # Choose a single random movie title using numpy's random.choice
    random_movie_title = np.random.choice(all_movie_titles, size=1, replace=False)[0]
    # print(random_movie_title)
    # Get movie details using your function (replace GetMovieFromName with your actual function)
    random_movie_detail = GetMovieFromName(random_movie_title)

    if random_movie_detail and 'imdbID' in random_movie_detail:
        allDetails = GetMovieFromID(random_movie_detail['imdbID'])

        with col6:
            # Display the poster image
            st.image(random_movie_detail['Poster'])

        with col7:
            # Display the random movie title
            Title = random_movie_detail['Title']
            st.markdown(f'<div style="font-weight: bold; font-size: 30px ;">Title:&nbsp;{Title}</div><br>',unsafe_allow_html=True)
            Release_year = random_movie_detail['Year']
            st.markdown(f'<div style="font-weight: bold;">Release year:&nbsp;{Release_year}</div><br>', unsafe_allow_html=True)
            imdbID = random_movie_detail['imdbID']
            st.markdown(f'<div style="font-weight: bold;">IMDB id:&nbsp;{imdbID}</div><br>', unsafe_allow_html=True)

            # Check if 'genres' key exists in allDetails
            if 'genres' in allDetails:
                genre_names = [genre['name'] for genre in allDetails['genres']]
                genre = ", ".join(genre_names)
                st.markdown(f'<div style="font-weight: bold;">Genres:&nbsp;{genre}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="font-weight: bold;">Genres:&nbsp;N/A</div>', unsafe_allow_html=True)
                
            overview = (allDetails['overview'] if 'overview' in allDetails else '')
            st.markdown('<div style="font-weight: bold; font-size: 20px;">Overview:</div>', unsafe_allow_html=True)
            st.write('')  # Add some space
            st.markdown(f'<div style="word-wrap: break-word; max-width: 800px;">{overview}</div>', unsafe_allow_html=True)



    else:
        st.warning("Movie details not available.")

    st.write('---')  # Add a horizontal line for separation
    st.write('')  # Add some space

    # Movie Recommender System
    form = st.form(key='my_form')
    form.title(':robot_face: Movie Recommender system')
    selected_movie_name = form.selectbox('SEARCH YOUR MOVIE', movies_list['title'].values, key="search_movie")

    if form.form_submit_button('Search'):
        poster, recommendations = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        if len(recommendations) >= 1:
            with col1:
                form.text(recommendations[0])
                form.markdown(f'<img src="{poster[0]}" style="height:300px; width:200px;">', unsafe_allow_html=True)

        if len(recommendations) >= 2:
            with col2:
                form.text(recommendations[1])
                form.markdown(f'<img src="{poster[1]}" style="height:300px; width:200px;">', unsafe_allow_html=True)

        if len(recommendations) >= 3:
            with col3:
                form.text(recommendations[2])
                form.markdown(f'<img src="{poster[2]}" style="height:300px; width:200px;">', unsafe_allow_html=True)

        if len(recommendations) >= 4:
            with col4:
                form.text(recommendations[3])
                form.markdown(f'<img src="{poster[3]}" style="height:300px; width:200px;">', unsafe_allow_html=True)

        if len(recommendations) >= 5:
            with col5:
                form.text(recommendations[4])
                form.markdown(f'<img src="{poster[4]}" style="height:300px; width:200px;">', unsafe_allow_html=True)

    # st.markdown("""<br><br>""")
    st.write("---")
    st.write("")
    # Displaying other movies
    st.subheader("\n:film_projector: All time favourites")
    random_movie_title2 = np.random.choice(all_movie_titles, size=5, replace=False)
    other_movie_details = [GetMovieFromName(title) for title in random_movie_title2]

    col_movies = st.columns(5)

    for i in range(5):
        col = col_movies[i]
        if other_movie_details[i] and 'Poster' in other_movie_details[i]:
            col.text(random_movie_title2[i])
            # Adjust height and width of the poster image
            col.markdown(f'<img src="{other_movie_details[i]["Poster"]}" style="height:300px; width:200px;">',
                         unsafe_allow_html=True)
        else:
            continue

current_memory = tracemalloc.get_traced_memory()
print("Current memory:", current_memory)

# Stop tracing memory allocations
tracemalloc.stop()

if __name__ == "__main__":
    main()

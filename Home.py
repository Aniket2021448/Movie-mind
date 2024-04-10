from streamlit_option_menu import option_menu
import streamlit as st
import pickle
from urllib.parse import quote
import requests
import numpy as np

import tracemalloc
tracemalloc.start()
# ,m,

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


api_key = 'b084b05d8a33512cad0a27d352fba9c4'

def get_movie_detailsFromName(movie_name):
    # Base URL for TMDb API
    base_url = "https://api.themoviedb.org/3"

    # Endpoint for searching movies by name
    search_endpoint = "/search/movie"

    # Parameters for the request
    params = {
        'api_key': api_key,
        'query': movie_name
    }

    # Send GET request to search for the movie
    response = requests.get(base_url + search_endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()

        # Check if there are any results
        if data['total_results'] > 0:
            # Get details of the first movie in the results
            movie_details = data['results'][0]
            return movie_details
        else:
            return "No movie found with that name."
    else:
        return "Error: Unable to retrieve data."





def getGenreNames(movie_genre_ids):

    # Define the base URL for TMDb API
    base_url = "https://api.themoviedb.org/3"

    # Endpoint for retrieving genre list
    genre_endpoint = "/genre/movie/list"

    # Parameters for the request
    params = {
    'api_key': api_key  # Replace 'YOUR_API_KEY' with your actual TMDb API key
    }

    # Send GET request to retrieve genre list
    response = requests.get(base_url + genre_endpoint, params=params)

    # Check if the request was successful
    if response.status_code == 200:
    # Parse JSON response
        data = response.json()

        # Extract genre names from genre IDs
        genre_names = {genre['id']: genre['name'] for genre in data['genres']}

        # Extract genre names for the given movie's genre IDs
        # movie_genre_ids = [28, 878]  # Example genre IDs from the provided data
        movie_genre_names = [genre_names[genre_id] for genre_id in movie_genre_ids]

        return ", ".join(movie_genre_names)
         
    else:
        return "Error: Unable to retrieve genre list."
        



def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    fetched_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommend_movies = []
    posters = []

    for j in fetched_movies[1:6]:
        movieDataFetched = get_movie_detailsFromName(movies_list.iloc[j[0]].title)
        if movieDataFetched and 'poster_path' in movieDataFetched:
            posters.append("https://image.tmdb.org/t/p/w500"+movieDataFetched['poster_path'])
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
    # Get movie details using your function (replace get_movie_detailsFromName with your actual function)
    random_movie_detail = get_movie_detailsFromName(random_movie_title)

    if random_movie_detail and 'id' in random_movie_detail:
        

        with col6:
            # Display the poster image
            st.image("https://image.tmdb.org/t/p/w500"+random_movie_detail['poster_path'])

        with col7:
            # Display the random movie title
            Title = random_movie_detail['title']
            st.markdown(f'<div style="font-weight: bold; font-size: 30px;">Title:&nbsp;{Title}</div><br>',unsafe_allow_html=True)
            
            Movie_genre = getGenreNames(random_movie_detail['genre_ids'])
            st.markdown(f'<div style="font-weight: bold;">Genres:&nbsp;{Movie_genre}</div>', unsafe_allow_html=True)

            popularity = random_movie_detail['popularity']
            st.markdown(f'<div style="font-weight: bold;">Popularity:&nbsp;{popularity}</div>', unsafe_allow_html=True)
           
            rating = random_movie_detail['vote_average']
            st.markdown(f'<div style="font-weight: bold;">Rating:&nbsp;{rating}</div>', unsafe_allow_html=True)
            
            Release_date = random_movie_detail['release_date']
            st.markdown(f'<div style="font-weight: bold;">Release year:&nbsp;{Release_date}</div><br>',unsafe_allow_html=True)
            
            overview = random_movie_detail['overview']
            st.markdown(f'<div style="font-weight: bold;">Overview:&nbsp;{overview}</div>', unsafe_allow_html=True)



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

    # Create a single column to contain all recommendations
        col_recommendations = st.columns(len(recommendations))

        for i in range(len(recommendations)):
            with col_recommendations[i]:
                st.text(recommendations[i])
                st.markdown(f'<img src="{poster[i]}" style="height:300px; width:200px;">', unsafe_allow_html=True)

    # st.markdown("""<br><br>""")
    st.write("---")
    st.write("")
    # Displaying other movies
    st.subheader("\n:film_projector: All time favourites")
    random_movie_title2 = np.random.choice(all_movie_titles, size=5, replace=False)
    other_movie_details = [get_movie_detailsFromName(title) for title in random_movie_title2]

    col_movies = st.columns(5)

    for i in range(5):
        col = col_movies[i]
        if other_movie_details[i] and 'poster_path' in other_movie_details[i]:
            col.text(random_movie_title2[i])
            # Adjust height and width of the poster image
            col.markdown(f'<img src="{"https://image.tmdb.org/t/p/w500"+other_movie_details[i]["poster_path"]}" style="height:300px; width:200px;">',
                         unsafe_allow_html=True)
        else:
            continue

    
    
    with st.form("app_selection_form"):
        st.write("Feel free to explore my other apps")
        app_links = {
            "find-the-fake": "https://find-fake-news.streamlit.app/",
            "Comment-Feel": "https://huggingface.co/spaces/GoodML/Comment-Feel"
        }
        selected_app = st.selectbox("Choose an App", list(app_links.keys()))

        submitted_button = st.form_submit_button("Go to App")

    # Handle form submission
    if submitted_button:
        selected_app_url = app_links.get(selected_app)
        if selected_app_url:
            st.success("Redirected successfully!")
            st.markdown(f'<meta http-equiv="refresh" content="0;URL={selected_app_url}">', unsafe_allow_html=True)

    
    # Dropdown menu for other app links

    st.write("In case the apps are down, because of less usage")
    st.write("Kindly reach out to me @ aniketpanchal1257@gmail.com")
    

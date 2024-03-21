import requests

# Replace 'YOUR_API_KEY' with your actual TMDb API key
api_key = 'b084b05d8a33512cad0a27d352fba9c4'

def get_movie_details(movie_name):
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


# Example usage
movie_name = "The Matrix"
movie_details = get_movie_details(movie_name)
print(movie_details)

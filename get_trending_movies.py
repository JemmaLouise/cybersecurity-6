import requests

# Your TMDb API key
api_key = '5691975e0ec0ebc572e6952891fa1124'

# URL to get the trending movies of the day
url = f'https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}'

# Make a request to the TMDb API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    trending_movies = response.json()

    # Print the trending movies data
    for movie in trending_movies['results']:
        print(f"Title: {movie['title']}, Release Date: {movie['release_date']}")
else:
    print(f"Failed to fetch data: {response.status_code}")

# Save the JSON response to a file
with open('trending_movies.json', 'w') as f:
    f.write(response.text)

print("Trending movies data saved to trending_movies.json")

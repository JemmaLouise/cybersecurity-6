# ScreenSort: Movie Recommendation System
## Overview
ScreenSort, A Movie Recommendation System, is a Python-based application that provides personalised movie suggestions to users based on their viewing history and preferences. The system utilizes data from The Movie Database (TMDb) API and incorporates machine learning techniques to recommend movies that align with user tastes.

## Features
- User Authentication and Profile Management: Users can sign up, log in, and manage their profiles, including setting preferences and maintaining a watch history.
- Personalized Movie Recommendations: Leverages machine learning algorithms to suggest movies based on genres, popularity, and user ratings.
- Search and Filter Functionality: Users can search for movies and filter results by genre, rating, and release year.
- Movie Details: Fetches and displays detailed information about movies, including descriptions, ratings, and trailers.
- Integration with TMDb API: Fetches up-to-date movie data, including genres, popularity, and ratings.

## Requirements 

Please see Requirements.txt for the full list of dependancies and requirements needed for ScreenSort to run. 

## How To Use 

1. ScreenSort is built to run through Python console in this stage with HTML templates and CSS for basic design.
2. You will need to ensure that you have all the requirements file programmes installed and change your details in the config file on line 5 to your own username and password from MySQL. If running through a virtual environment, you will need to export your TMDB API key. NOTE: There is a ‘Secret Key’ in this file as a protection against clients altering the content.
3. You will need to ensure that there is a connection between PyCharm and MySQL Workbench (or your own SQL programme) to use the models file; alternatively, you can make the database and corresponding tables in SQL.
4. Run Flask first then the main App file.


# add_movies.py

import os
import django
from datetime import datetime
from projectapp.models import Movie
from django.contrib.auth.models import User

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Project.settings')
django.setup()

def add_movies():
    # Sample movie data
    movies_data = [
        {
            'title': 'The Shawshank Redemption',
            'poster': 'https://www.example.com/posters/the_shawshank_redemption.jpg',
            'description': 'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
            'release_date': datetime(1994, 10, 14).date(),
            'actors': 'Tim Robbins, Morgan Freeman',
            'category': 'Drama',
            'trailer_link': 'https://www.youtube.com/watch?v=6hB3S9bIaco',
        },
        # Add details for the remaining movies similarly
        # Repeat this block for each movie
    ]

    # Assuming there's a default user to add movies
    user = User.objects.first()

    # Add movies to the database
    for movie_data in movies_data:
        movie = Movie.objects.create(
            title=movie_data['title'],
            poster=movie_data['poster'],
            description=movie_data['description'],
            release_date=movie_data['release_date'],
            actors=movie_data['actors'],
            category=movie_data['category'],
            trailer_link=movie_data['trailer_link'],
            added_by=user
        )
        print(f"Added movie: {movie.title}")

if __name__ == '__main__':
    add_movies()

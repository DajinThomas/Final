# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .models import Movie, Review
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import MovieForm
from datetime import datetime, timedelta


def home(request):
    # Fetch all movies
    all_movies = Movie.objects.all()

    # Calculate the date range for the past week
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)

    # Filter movies released in the last one week
    new_movies = Movie.objects.filter(release_date__gte=one_week_ago)

    # Setting minimum review rate for popular movies
    minimum_review_rate = 2

    # Filter popular movies based on review rating
    popular_movies = Movie.objects.filter(average_rating__gte=minimum_review_rate)

    # Fetch unique categories
    unique_categories = Movie.objects.values_list('category', flat=True).distinct()

    return render(request, 'home.html', {
        'all_movies': all_movies,
        'new_movies': new_movies,
        'popular_movies': popular_movies,
        'unique_categories': unique_categories
    })
@login_required
def add_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        poster = request.POST['poster']
        description = request.POST['description']
        release_date = request.POST['release_date']
        actors = request.POST['actors']
        category = request.POST['category']
        trailer_link = request.POST['trailer_link']
        added_by = request.user
        Movie.objects.create(title=title, poster=poster, description=description, release_date=release_date,
                              actors=actors, category=category, trailer_link=trailer_link, added_by=added_by)
        return redirect('home')
    return render(request, 'add_movie.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the login page after logout


@login_required
def view_profile(request):
    # Filter movies based on the logged-in user
    movies = Movie.objects.filter(added_by=request.user)
    return render(request, 'profile.html', {'movies': movies})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('view_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})


from .forms import ReviewForm


def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_detail', movie_id=movie_id)
    else:
        form = ReviewForm()
    return render(request, 'home.html', {'form': form})

def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})

def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('view_profile')
    return render(request, 'confirm_delete_movie.html', {'movie': movie})
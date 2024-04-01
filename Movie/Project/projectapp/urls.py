from django.urls import path
from .views import (
    home,
    add_movie,
    register,
    login_view,
    logout_view,
    view_profile,
    edit_profile,
    change_password,  # Import the MovieDetailView
    movie_detail,
    add_review,
    delete_movie,
    edit_movie,
)

urlpatterns = [
    path('', home, name='home'),
    path('add_movie/', add_movie, name='add_movie'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', view_profile, name='view_profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('profile/change_password/', change_password, name='change_password'),
    path('movie/<int:movie_id>/', movie_detail, name='movie_detail'),
    path('movie/<int:movie_id>/add_review/', add_review, name='add_review'),
    path('delete_movie/<int:movie_id>/', delete_movie, name='delete_movie'),
    path('edit_movie/<int:movie_id>/', edit_movie, name='edit_movie'),
]

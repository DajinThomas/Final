# models.py
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Movie(models.Model):
    objects = None
    title = models.CharField(max_length=100)
    poster = models.URLField()
    description = models.TextField()
    release_date = models.DateField()
    actors = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    trailer_link = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0)


class Review(models.Model):
    objects = None
    content = models.TextField()
    rating = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_movie_average_rating(sender, instance, **kwargs):
    movie = instance.movie
    average_rating = Review.objects.filter(movie=movie).aggregate(Avg('rating'))['rating__avg']
    if average_rating is not None:
        movie.average_rating = round(average_rating, 1)
    else:
        movie.average_rating = 0
    movie.save()

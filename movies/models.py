from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=50)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class MovieComment(models.Model):
    rating_choices = ((5, 'Five points'),(4, 'Four points'),(3, 'Three points'),(2, 'Two points'),(1, 'One point'))
    rating = models.IntegerField(choices=rating_choices)
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_comments')

    def __str__(self):
        return self.content
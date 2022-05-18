from django.db import models


# Create your models here.
class Genre(models.Model):
    name = models.TextField()


class Spokenlanguage(models.Model):
    name = models.CharField(max_length=20)


class Productioncountry(models.Model):
    name = models.CharField(max_length=20)


class Collection(models.Model):
    name = models.CharField(max_length=40)


class Movie(models.Model):
    title = models.CharField(max_length=20)
    poster_path = models.TextField()
    overview = models.TextField()
    genre_ids = models.ManyToManyField(Genre, related_name='movie_genre')
    language_ids = models.ManyToManyField(Spokenlanguage, related_name='movie_spokenlanguage')
    productioncountry_ids = models.ManyToManyField(Productioncountry, related_name='movie_productioncountry')
    collection_ids = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='movies')

    def __str__(self):
        return self.title

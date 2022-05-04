from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models

from account.models import CustomUser
from liked.models import Like


class Category(models.Model):
    name = models.CharField(max_length=150, unique=False)
    slug = models.SlugField(max_length=100, primary_key=True)


    def __str__(self):
        return self.name


class Movie(models.Model):

    title = models.CharField(max_length=40, unique=True)
    actor = models.CharField(max_length=100)
    genre = models.CharField(max_length=70)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='films')
    img = models.ImageField(upload_to='images', null=True)
    description = models.TextField()
    # likes = GenericRelation(Like)
    body = models.CharField(max_length=140)

    def __str__(self):
        return self.body

    @property
    def total_likes(self):
        return self.likes.count()


class MovieReview(models.Model):

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews', null=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1)
    # likes = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)



class Favorites(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liked')

    class Meta:
        unique_together = ['movie', 'user']

class MoviePlay(models.Model):
    film = models.FileField(upload_to='videos', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='videos')














































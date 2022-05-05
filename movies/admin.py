from django.contrib import admin

from .models import Category, Movie, MoviePlay, Rating, Like, Comment

admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(MoviePlay)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Comment)
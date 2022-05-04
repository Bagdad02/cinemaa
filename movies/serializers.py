from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

import liked
from .models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MovieSerializer(ModelSerializer):
    is_fan = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['rating'] = MovieReview.objects.all().aggregate(Avg('rating'))
        representation['body'] = MoviePlaySerializer(instance.videos.all(), context=self.context, many=True).data
        return representation

    def get_is_fan(self, obj):
        user = self.context.get('request').user
        return liked.services.is_fan(obj, user)


class MovieReviewSerializer(ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(),
                                               write_only=True)
    movie_title = serializers.SerializerMethodField("get_movie_title")
    rating = serializers.IntegerField()

    class Meta:
        model = MovieReview
        fields = "__all__"

    def get_movie_title(self, movie_review):
        title = movie_review.movie.title
        return title

    def validate_movie(self, movie):

        if self.Meta.model.objects.filter(movie=movie).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на этот фильм"
            )
        return movie

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5"
            )
        return rating

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['author'] = user
        review = MovieReview.objects.create(**validated_data)
        return review


class MoviePlaySerializer(ModelSerializer):
    class Meta:
        model = MoviePlay
        fields = '__all__'

# from django.db.models import Avg
# from rest_framework import serializers
#
# from movies.models import Category, Movie, MovieImage, Review
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'
#
# class MovieListSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()
#     user = serializers.CharField(source='user')
#
#     class Meta:
#         model = Movie
#         fields = '__all__'
#
#     def get_image(self, movie):
#         first_image = movie.pics.first()
#         # print(dir(first_image))
#         if first_image and first_image.image:
#             return first_image.image.url
#         return ''
#
#     def is_liked(self, movie):
#         user = self.context.get('request').user
#         return user.liked.filter(movie=movie).exists()
#
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['author'] = instance.user.email
#         representation['rating'] = Review.objects.all().aggregate(Avg('rating'))
#         user = self.context.get('request').user
#         if user.is_authenticated:
#             representation['is_liked'] = self.is_liked(instance)
#         return representation
#
#
#
# class ReviewSerializer(serializers.ModelSerializer):
#     movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(),
#                                                write_only=True)
#
#
#     class Meta:
#         model = Review
#         fields = '__all__'
#
#
#     def create(self, validated_data):
#         user = self.context.get('request').user
#         validated_data['user'] = user
#         return super().create(validated_data)
#
#     def validate_movie(self, movie):
#         user = self.context.get('request').user
#         if self.Meta.model.objects.filter(movie=movie).exists() and self.Meta.model.objects.filter(user=user).exists():
#             raise serializers.ValidationError("Вы уже ставили отзыв на этот фильм")
#         return movie
#
#     def validate_rating(self, rating):
#         if rating not in range(1, 6):
#             raise serializers.ValidationError(
#                 "Рейтинг должен быть от 1 до 5"
#             )
#         return rating
#
#
#
#
# class MovieImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MovieImage
#         fields = ['image']
#
# class MovieSerializer(serializers.ModelSerializer):
#     images = serializers.ListField(child=serializers.ImageField(allow_empty_file=False),
#                                    write_only=True, required=True)
#
#     class Meta:
#         model = Movie
#         exclude = ['user']
#
#     def create(self, validated_data):
#         user = self.context.get('request').user
#         validated_data['user'] = user
#         images = validated_data.pop('images', [])
#         movie = super().create(validated_data)
#         for image in images:
#             MovieImage.objects.create(movie=movie, image=image)
#         return movie
#
#     def update(self, instance, validated_data):
#         images = validated_data.pop('images', [])
#         if images:
#             for image in images:
#                 MovieImage.objects.create(movie=instance, image=image)
#         return super().update(instance, validated_data)
#
#     def is_liked(self, movie):
#         user = self.context.get('request').user
#         return user.likes.filter(movie=movie).exists()
#
#     def to_representation(self, instance):
#         representation = super(MovieSerializer, self).to_representation(instance)
#         representation['images'] = MovieImageSerializer(instance.pics.all(), many=True).data
#         representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
#         user = self.context.get('request').user
#         if user.is_authenticated:
#             representation['is_liked'] = self.is_liked(instance)
#         representation['likes_count'] = instance.favorites.count()
#         return representation
#

























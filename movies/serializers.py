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
        # representation['rating'] = MovieReview.objects.all().aggregate(Avg('rating'))
        representation['body'] = MoviePlaySerializer(instance.videos.all(), context=self.context, many=True).data
        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()
            representation['likes'] = instance.like.filter(like=True).count()
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


class RatingSerializers(serializers.Serializer):
    class Meta:
        model = Rating
        fields = '__all__'

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


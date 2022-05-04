from django.db.models import Q
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from account.permissions import IsActivePermission
# from liked.mixins import LikedMixin
from liked.mixins import LikedMixin
from movies.models import Category, Movie, Favorites, MovieReview, MoviePlay
from movies.permissions import IsAuthor
from movies.serializers import CategorySerializer, MovieSerializer, MovieReviewSerializer, MoviePlaySerializer
from movies.service import MovieFilter


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]


class MovieViewSet(ModelViewSet, LikedMixin):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [IsAuthenticated, ]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['title', 'text']
    filterset_fields = ['category', 'genre']


    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.queryset
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))
        serializer = MovieSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        movie = self.get_object()
        reviews = movie.reviews.all()
        serializer = MovieReviewSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data, status=200)

    def get_permissions(self):
        if self.action in ['create', 'add_to_favorites', 'remove_from_favorites']:
            return [IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthor()]
        return []


    @action(['POST'], detail=True)
    def add_to_favorites(self, request, pk=None):
        movie = self.get_object()
        if request.user.liked.filter(movie=movie).exists():
            return Response('Фильм уже находится в избранных')
        Favorites.objects.create(movie=movie, user=request.user)
        return Response('Добавлено в избранное')

    @action(['POST'], detail=True)
    def remove_from_favorites(self, request, pk=None):
        movie = self.get_object()
        if not request.user.liked.filter(movie=movie).exists():
            return Response('Фильм не находится в списке избранных')
        request.user.liked.filter(movie=movie).delete()
        return Response('Фильм удалён из избранных')


class MovieReviewViewSet(ModelViewSet):
    queryset = MovieReview.objects.all()
    serializer_class = MovieReviewSerializer
    permission_classes = [IsActivePermission]

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

class MoviePlayView(generics.ListCreateAPIView):
    queryset = MoviePlay.objects.all()
    serializer_class = MoviePlaySerializer

    def get_serializer_context(self):
        return {'request':self.request}




























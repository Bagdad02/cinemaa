from django_filters import rest_framework as filters

from movies.models import Movie


class CharFilterInFilter(filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name='category__name')
    class Meta:
        model = Movie
        fields = ['category']

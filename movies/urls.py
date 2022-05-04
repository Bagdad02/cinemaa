from django.urls import path, include
from rest_framework.routers import DefaultRouter
from movies.views import CategoryListView, MovieViewSet, MovieReviewViewSet

router = DefaultRouter()
router.register('movie', MovieViewSet)
router.register('reviews', MovieReviewViewSet)


urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('', include(router.urls))

]

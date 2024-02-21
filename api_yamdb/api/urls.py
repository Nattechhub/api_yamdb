from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    UsersViewSet,
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewsViewSet,
    CommentsViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register(
    r'users',
    UserViewSet,
    basename='user'
)
router.register(r'users', UsersViewSet, 'users')

urlpatterns = [
    path('', include(router.urls)),
]

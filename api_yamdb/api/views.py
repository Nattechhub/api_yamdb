from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import action
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .filters import TitleFilter
from .permissions import (
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly,
    IsAdmin,
    IsOwner
)
from titles.models import Title, Category, Genre
from reviews.models import Review
from users.models import User
from .serializers import (
    UserSerializer,
    UserRetrieveSerializer,
    MeSerializer,
    TitleListRetrieveSerializer,
    TitleCreateUpdateDestroySerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewsSerializer,
    CommentsSerializer
)


class TitleViewSet(viewsets.ModelViewSet):
    """Обрабатываем запросы к /titles."""
    queryset = Title.objects.annotate(rating=(Avg('reviews__score')))
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleListRetrieveSerializer
        return TitleCreateUpdateDestroySerializer


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Обрабатываем запросы к /categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_fields = ['slug']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, slug=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Обрабатываем запросы к /genres."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_fields = ['slug']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def destroy(self, request, pk=None):
        genre = get_object_or_404(Genre, slug=pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewsViewSet(viewsets.ModelViewSet):
    """Обрабатываем запросы к /reviews/.*$."""
    serializer_class = ReviewsSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    """Обрабатываем запросы к /comments/.*$."""
    serializer_class = CommentsSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)


class UsersViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Обрабатываем запросы к /users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    permission_classes = (IsAdmin,)


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Обрабатываем запросы к /users/{username}."""
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsAdmin,)
    pagination_class = None
    http_method_names = ['get', 'patch', 'delete']
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        return User.objects.filter(username=username)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsOwner],
    )
    def me(self, request):
        """Обрабатываем запросы к /users/me."""
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = MeSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

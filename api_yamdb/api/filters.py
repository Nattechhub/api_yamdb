from django_filters import FilterSet, CharFilter
from titles.models import Title


class TitleFilter(FilterSet):
    """
    Используется для фильтрации Категорий и Жанров.
    """
    genre = CharFilter(
        field_name='genre__slug',
        lookup_expr='exact',
    )
    category = CharFilter(
        field_name='category__slug',
        lookup_expr='exact',
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')

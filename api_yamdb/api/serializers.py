from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.validators import RegexValidator
from titles.models import Title, Category, Genre
from reviews.models import Review, Comments
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Основной серализатор для запросов list, create на эндпоинт /users/"""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class UserRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов retrieve, patch, delete
    на эндпоинт /users/{username}.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class MeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов retrieve, patch
    на эндпоинт /users/me.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )
    email = serializers.EmailField(max_length=254)
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def get_role(self, obj):
        """
        Используется для ограничения изменение поля role.
        В запрос добавляется поле role с текущим значение,
        вне зависимости от значения переданого в запросе.
        """
        return obj.role


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов list, create, delete
    на эндпоинт /genres.
    """

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов list, create, delete
    на эндпоинт /categories.
    """

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleCreateUpdateDestroySerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов на эндпоинт /titles и /titles/{pk}.
    Разрешенные методы - create, update и destroy.
    """
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('__all__')


class TitleListRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов на эндпоинт /titles и /titles/{pk}.
    Разрешенные методы - list и retrieve.
    """
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.DecimalField(
        read_only=True,
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False
    )

    class Meta:
        model = Title
        fields = ('__all__')


class ReviewsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов на эндпоинт /reviews и /reviews/{pk}.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    title = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all(),
        default=None,
        write_only=True
    )

    def validate_title(self, value):
        """
        Забираем идентификатор произведения
        для заполнения поля.
        """
        return self.context['view'].kwargs['title_id']

    class Meta:
        model = Review
        fields = ('__all__')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message="Можно оставить только один отзыв."
            )
        ]


class CommentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор для запросов на эндпоинт /comments и /comments/{pk}.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comments
        exclude = ['review']

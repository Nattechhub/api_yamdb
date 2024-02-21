import datetime as dt
from django.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)


class Genre(models.Model):
    """Модель для хранения Жанров."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель для хранения Категорий."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель для хранения Произведений."""
    name = models.CharField(max_length=256)
    year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(
                dt.datetime.now().year,
                message="Год выпуска не может быть больше текущего"
            )
        ]
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.genre} {self.title}'

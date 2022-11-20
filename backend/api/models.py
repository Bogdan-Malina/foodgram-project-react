from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

from colorfield.fields import ColorField

User = get_user_model()


class Ingredient(models.Model):

    name = models.CharField(
        'Название',
        max_length=200
    )

    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200
    )

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )

    color = ColorField(
        'Цвет',
        unique=True,
        default='#FF0000'
    )

    slug = models.SlugField(
        'Слуг',
        max_length=200,
        unique=True,
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.slug


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )

    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )

    image = models.ImageField(
        'Картинка',
        upload_to='recipes/'
    )

    text = models.TextField(
        'Описание'
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        verbose_name='Ингридиенты',
        related_name='recipes',
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )

    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Не введено время'),),
        verbose_name='Время приготовления')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            validators.MinValueValidator(
                1, message='Не введено колличество ингредиентов'),),
        verbose_name='Количество',
    )

    class Meta:
        ordering = ['-id']


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт',
    )

    class Meta:
        ordering = ['-id']

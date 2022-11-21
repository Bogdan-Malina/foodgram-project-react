from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from .models import Recipes, Tag

User = get_user_model()


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipesFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipes
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(favorites__user=user)
        return Recipes.objects.all()

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user

        if value:
            return queryset.filter(cart__user=user)
        return Recipes.objects.all()

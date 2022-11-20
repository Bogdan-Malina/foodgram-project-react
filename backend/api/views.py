from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.http import HttpResponse
import csv
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import RecipesFilter, IngredientSearchFilter
from api.models import (
    ShoppingList,
    Favorite,
    Ingredient,
    Recipes,
    Tag,
    IngredientAmount
)
from api.pagination import CustomPageNumberPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly

from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
)


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


def add(model, user, pk):
    obj = model.objects.filter(
        user=user,
        recipe=pk
    ).exists()

    detail = {'errors': 'Рецепт уже добавлен'}

    if obj:
        return Response(
            detail,
            status=status.HTTP_400_BAD_REQUEST
        )

    recipe = Recipes.objects.get(id=pk)
    model.objects.create(
        user=user,
        recipe=recipe
    )
    serializer = RecipeSerializer(recipe)
    return Response(
        serializer.data,
        status=status.HTTP_201_CREATED
    )


def delete(model, user, pk):
    obj = model.objects.filter(
        user=user,
        recipe=pk
    )

    detail = {'errors': 'Рецепт уже удален'}

    if obj.exists():
        obj.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
    return Response(
        detail,
        status=status.HTTP_400_BAD_REQUEST
    )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipesFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=[
            'post',
            'delete'
        ],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return add(
                Favorite,
                request.user,
                pk
            )
        elif request.method == 'DELETE':
            return delete(
                Favorite,
                request.user,
                pk
            )

    @action(
        detail=True,
        methods=[
            'post',
            'delete'
        ],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return add(
                ShoppingList,
                request.user,
                pk
            )
        elif request.method == 'DELETE':
            return delete(
                ShoppingList,
                request.user,
                pk
            )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        user = self.request.user
        ingredient_list = []

        if user.is_anonymous:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = IngredientAmount.objects.filter(
            recipe__cart__user=request.user
        )

        for ingredient in data:
            ingredient_list.append(
                [
                    ingredient.ingredient.name,
                    ingredient.amount,
                    ingredient.ingredient.measurement_unit
                ]
            )
        ingredient_list.sort()

        previous_ingredient = 0
        duplicate_index_list = []

        for i in range(1, len(ingredient_list)):
            if ingredient_list[i][0] == ingredient_list[previous_ingredient][0]:
                ingredient_list[i][1] = ingredient_list[i][1] + ingredient_list[previous_ingredient][1]
                duplicate_index_list.append(ingredient_list[previous_ingredient])
            previous_ingredient += 1

        for duplicate_index in duplicate_index_list:
            ingredient_list.remove(duplicate_index)

        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)

        for ingredient in list(ingredient_list):
            writer.writerow(ingredient)
        return response

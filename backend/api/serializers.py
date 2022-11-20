from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Ingredient, IngredientAmount, Recipes, Tag
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


def is_in_favorited_and_shopping_card(data, user):
    is_in_favorited = Recipes.objects.filter(
        favorites__user=user,
        id=data.id
    ).exists()

    if is_in_favorited:
        data.is_favorited = is_in_favorited

    is_shopping_cart = Recipes.objects.filter(
        cart__user=user,
        id=data.id
    ).exists()
    if is_shopping_cart:
        data.is_in_shopping_cart = is_shopping_cart
    return data


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(
        source='ingredientamount_set',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.BooleanField(default=False)
    is_in_shopping_cart = serializers.BooleanField(default=False)

    class Meta:
        model = Recipes
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def to_representation(self, instance):
        if self.context:
            user = self.context.get('request').user
            instance = is_in_favorited_and_shopping_card(
                instance, user
            )
        data = super().to_representation(instance)
        return data

    # def shopping_cart(self, request, pk=None):
    #     print()
    #     # if request.method == 'POST':
    #     #     return self.add_obj(Cart, request.user, pk)
    #     # elif request.method == 'DELETE':
    #     #     return self.delete_obj(Cart, request.user, pk)
    #     # return None

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Ошибка'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = get_object_or_404(Ingredient,
                                           id=ingredient_item['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                        'Ошибка'
                    )
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': ('Убедитесь, что значение количества '
                                    'ингредиента больше 0')
                })
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data):
        validated_data.pop('is_favorited')
        validated_data.pop('is_in_shopping_cart')
        ingredients_data = validated_data.pop('ingredients')

        recipe = Recipes.objects.create(
            **validated_data,
        )

        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)

        for ingredient_data in ingredients_data:
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_data.get('id'),
                amount=ingredient_data.get('amount'),
            )

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name',
            instance.name
        )
        instance.text = validated_data.get(
            'text',
            instance.text
        )
        instance.image = validated_data.get(
            'image',
            instance.image
        )
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )

        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)

        IngredientAmount.objects.filter(
            recipe=instance
        ).delete()

        for ingredient_data in validated_data.get('ingredients'):
            IngredientAmount.objects.create(
                recipe=instance,
                ingredient_id=ingredient_data.get('id'),
                amount=ingredient_data.get('amount'),
            )

        instance.save()
        return instance

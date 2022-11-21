from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from .models import Follow

from api.models import Recipes

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'password',
            'username',
            'first_name',
            'last_name'
        )


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')


def get_recipes_count(obj):
    return obj.recipes.count()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'recipes',
            'recipes_count',
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        if self.context:
            user = self.context.get('request').user
            if user.is_anonymous:
                return False
            return Follow.objects.filter(user=user, author=obj.id).exists()

    def get_recipes(self, obj):
        if self.context:
            limit = self.context('request').query_params.get('recipes_limit')
            if limit is None:
                recipes = obj.recipes.all()
            else:
                recipes = obj.recipes.all()[:int(limit)]
            return FollowRecipeSerializer(recipes, many=True).data

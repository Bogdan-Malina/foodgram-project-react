from django.contrib import admin
from .models import ShoppingList, Favorite, Ingredient, Recipes, Tag
from users.models import User


def count(obj):
    return obj.favorites.count()


class UserAdmin(admin.ModelAdmin):
    list_filter = ('name', 'email')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count')
    list_filter = ('author', 'name', 'tags')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(ShoppingList)
admin.site.register(Favorite)

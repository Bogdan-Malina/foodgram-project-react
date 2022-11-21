from django.contrib import admin
from .models import ShoppingList, Favorite, Ingredient, Recipes, Tag

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class IngredientResource(resources.ModelResource):
   class Meta:
      model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count')
    list_filter = ('author', 'name', 'tags')

    def count(self, obj):
        return obj.favorites.count()


class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(ShoppingList)
admin.site.register(Favorite)

"""
URL mappings for the recipe API.
"""
from django.urls import (path, include)

from rest_framework.routers import DefaultRouter

from recipe import views

#With this function (router) you can have all methods (POST, GET, PUT, PATCH, DELETE)
router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),

]
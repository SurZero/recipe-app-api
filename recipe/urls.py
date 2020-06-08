from django.urls import path, include
from rest_framework.routers import DefaultRouter # automatically generates url for viewsets

from recipe import views

router = DefaultRouter()
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]


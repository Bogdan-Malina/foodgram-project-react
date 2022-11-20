from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet
# from .views import FollowViewSet

app_name = 'api'

router = DefaultRouter()
router.register('users', CustomUserViewSet)

urlpatterns = [
    # path('users/<int:following_id>/subscribe/', FollowViewSet.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
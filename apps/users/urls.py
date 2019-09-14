from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .views import index, UserViewset

urlpatterns = [
    path('auth/token/', obtain_jwt_token),
    path('auth/token/refresh/', refresh_jwt_token),
]

router = DefaultRouter()
router.register('users', UserViewset, basename='user')
urlpatterns += router.urls

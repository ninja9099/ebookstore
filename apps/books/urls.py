from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewset

urlpatterns = [
]

router = DefaultRouter()
router.register(r'users', UserViewset, basename='user')
urlpatterns += router.urls

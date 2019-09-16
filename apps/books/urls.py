from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.books.views import BookViewSet, CategoryViewSet


router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('books', BookViewSet, basename='book')
urlpatterns = router.urls

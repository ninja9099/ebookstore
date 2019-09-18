from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.books.views import BookViewSet, CategoryViewSet, book_review

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('books', BookViewSet, basename='book')
urlpatterns = [
    path('review/<int:book_id>', book_review, name='book-review')
]
urlpatterns += router.urls

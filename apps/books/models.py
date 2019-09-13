from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.books.constants import BookReadStatus
from apps.common.base_model import BaseModel
from apps.users.constants import UserTypes

User = get_user_model()


def limit_user_choices():
    return {'user_type': UserTypes.Reader}


def book_cover_path(instance, filename):
    """
    method to create separate folder for each user
    :param instance:
    :param filename:
    :return: file_path
    """
    return 'book_cover_{0}/{1}'.format(instance.id, filename)


class Category(models.Model):
    name = models.CharField(_("Category"), max_length=255)
    # for multi-level category structure support (self reference)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)


class Book(BaseModel):
    name = models.CharField(_("Book Title"), max_length=255)
    cover = models.ImageField(upload_to=book_cover_path)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    # author can be multiple
    author = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='books_written_set',
        related_query_name='book_writers',
    )
    total_pages = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "eb_book"
        verbose_name = "Book"
        # to order with alphabetically
        order_with_respect_to = 'name'

    def __str__(self):
        reviews_list = self.book_reviews_set.aggregate(Avg('rating'))
        print(reviews_list)
        avg_rating = float(reviews_list['rating__avg'])
        return "{} --> {}".format(self.name, avg_rating)


class BookReview(BaseModel):
    book = models.ForeignKey(Book, related_name='book_reviews_set', on_delete=models.CASCADE)
    review = models.CharField(max_length=2048, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(User, limit_choices_to=limit_user_choices, on_delete=models.CASCADE)

    class Meta:
        db_table = "eb_book_reviews"
        verbose_name = "Book Review"

    def __str__(self):
        return "{}:{}".format(self.book.name, self.user)


class UserReadingHistory(BaseModel):
    book = models.ForeignKey(Book, related_name='user_read_set', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="books_readed", limit_choices_to=limit_user_choices, on_delete=models.CASCADE)
    page_no = models.IntegerField(default=1)
    status = models.IntegerField(choices=BookReadStatus.get_choices(), default=BookReadStatus.Started)
    total_pages = models.IntegerField()
    time_spent = models.TimeField(blank=True, null=True)

    class Meta:
        db_table = "eb_user_reading_history"
        verbose_name = "User Reading History"

    def __str__(self):
        return "{}:{}".format(self.book.name, self.user.username)

    def __repr__(self):
        return "<{} for {}, {}>".format(self.__class__.__name__, self.book.name, self.user)


class UserBookSessions(BaseModel):
    book = models.ForeignKey(Book, related_name='user_book_session_set', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_sessions", limit_choices_to=limit_user_choices,
                             on_delete=models.CASCADE)

    class Meta:
        db_table = "eb_user_reading_sessions"
        verbose_name = "User Reading sessions"

    def __str__(self):
        return "{}:{}".format(self.user.username, self.book.name)

    def __repr__(self):
        return "<{} for {}, {}>".format(self.__class__.__name__, self.book.name, self.user)

import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.books.constants import BookReadStatus
from apps.common.base_model import BaseModel
from apps.users.constants import UserTypes

User = get_user_model()


def limit_user_choices():
    return {'user_type': UserTypes.Reader}


def get_dir_path(instance, filename):
    return "books/{}_{}".format(instance.name, filename)


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
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='child_set', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)


class Book(BaseModel):
    name = models.CharField(_("Book Title"), max_length=255)
    cover = models.ImageField(upload_to=book_cover_path)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    # author can be multiple but as of now only primary author can be linked
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='books_written_set',on_delete=models.CASCADE
    )
    published_date = models.DateField()
    total_pages = models.IntegerField(blank=True, null=True)
    publisher = models.CharField(max_length=1024)
    file = models.FileField(upload_to=get_dir_path)
    slug = models.SlugField(unique=True, blank=True)


    class Meta:
        db_table = "eb_book"
        verbose_name = "Book"
        # to order with alphabetically
        order_with_respect_to = 'name'

    @property
    def get_rating(self):
        reviews_list = self.book_reviews_set.aggregate(Avg('rating'))
        if reviews_list['rating__avg']:
            avg_rating = float(reviews_list['rating__avg'])
        else:
            avg_rating = 0
        return avg_rating

    def __str__(self):
        return "{}".format(self.name)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Book, self).save(*args, **kwargs)

class BookReview(BaseModel):
    book = models.ForeignKey(Book, related_name='book_reviews_set', on_delete=models.CASCADE)
    review = models.CharField(max_length=2048, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(User, limit_choices_to=limit_user_choices, on_delete=models.CASCADE)

    class Meta:
        db_table = "eb_book_reviews"
        verbose_name = "Book Review"
        unique_together = ('book', 'user')
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
        return "{}:{}".format(self.book.name, self.user)

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
        return "{}:{}".format(self.user, self.book.name)

    def __repr__(self):
        return "<{} for {}, {}>".format(self.__class__.__name__, self.book.name, self.user)

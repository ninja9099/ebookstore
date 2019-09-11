from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models

from apps.common.base_model import BaseModel


def limit_pub_date_choices():
    return {'profile__type': 2}


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
    parent = models.ForeignKey("self", on_delete=models.SET_NULL())


class Book(BaseModel):
    name = models.CharField(_("Book Title"), max_length=255)
    cover = models.ImageField(upload_to=book_cover_path)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL)
    # author can be multiple
    author = models.ManyToManyField(
        _("Writer"),
        to='User',
        related_name='books_written_set',
        related_query_name='book_writers',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = "eb_book"
        verbose_name = "Book"
        # to order with alphabetically
        order_with_respect_to = 'name'


class BookReview(BaseModel):
    book = models.ForeignKey(Book, related_name='book_reviews_set', on_delete=models.CASCADE)
    review = models.CharField(max_length=2048, blank=True, null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(User, limit_choices_to=limit_pub_date_choices)
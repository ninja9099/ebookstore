from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.


class Book(models.Model):

    class Meta:
        db_table = "eb_book"
        verbose_name_plural = "Books"

    name = models.CharField(_("Book Title"), max_length=255)
    category models.ForeignKey(Category, on_delete=models.SET_DEFAULT(11))
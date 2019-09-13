from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(BookReview)
admin.site.register(UserReadingHistory)
admin.site.register(UserBookSessions)
# Generated by Django 2.2.5 on 2019-09-18 19:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0007_auto_20190917_1822'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='bookreview',
            unique_together={('book', 'user')},
        ),
    ]

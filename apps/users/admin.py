from django.contrib import admin

# Register your models here.
from apps.users.models import User, EmailVerificationTokens

admin.site.register(User)
admin.site.register(EmailVerificationTokens)
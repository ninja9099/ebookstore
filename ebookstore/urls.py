"""ebookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from apps.users.views import index, verify_email, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('logout/', user_logout, name='logout'),
    path('verify_email/', verify_email, name='verify-email'),
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.books.urls')),
    path('openapi', get_schema_view(
        title="E-bookStore",
        description="API for all things",
        version="1.0.0",
        urlconf='ebookstore.urls'
    ), name='schema'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url':'schema'}
    ), name='swagger-ui'),
]
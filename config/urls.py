import os

from rest_framework.routers import SimpleRouter
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.conf.urls.static import static

from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="SHOP API",
        default_version='v1',
    ),
    public=True,
)

urlpatterns = [
    path('docs/', schema_view.with_ui('swagger')),
    path('admin/', admin.site.urls),
    path('api/v1/account/', include('account.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


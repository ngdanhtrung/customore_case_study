"""
URL configuration for delivery project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

import os

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from delivery.services import health_check
from delivery.services.auth import view as auth_view
from delivery.services.tasks import view as task_view
from rest_framework.routers import DefaultRouter

routers = DefaultRouter(trailing_slash=False)
routers.register(r"user", auth_view.AuthViewSet, basename="user")
routers.register(r"task", task_view.TasksAPIViewSet, basename="task")

urlpatterns = [
    # YOUR PATTERNS
    path("schema", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("admin/", admin.site.urls),
    path("health-check", health_check.HealthCheckView.as_view(), name="health-check"),
    path("api/v1/", include(routers.urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

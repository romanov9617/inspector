"""
URL configuration for school project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from admin_modules.defects.urls import urlpatterns as defects_urls
from admin_modules.media.urls import urlpatterns as media_urls
from admin_modules.ml_models.urls import urlpatterns as ml_models_urls
from admin_modules.oidc.views import HealthCheckView
from admin_modules.oidc.views import JWKSView
from admin_modules.oidc.views import OpenIDConfigurationView
from admin_modules.reports.urls import urlpatterns as report_urls
from django.contrib import admin
from django.urls import include
from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

from admin.settings import REGULAR_API_PREFIX

urlpatterns = [
    path("admin/", admin.site.urls),
    path(".well-known/openid-configuration", OpenIDConfigurationView.as_view(), name="openid-config"),
    path("jwks.json", JWKSView.as_view(), name="jwks"),
    path(f"{REGULAR_API_PREFIX}health/", HealthCheckView.as_view(), name="health-check"),
    path(f'{REGULAR_API_PREFIX}auth/users/', include('djoser.urls')),
    path(f'{REGULAR_API_PREFIX}auth/', include('djoser.urls.jwt')),
    path(f"{REGULAR_API_PREFIX}schema/", SpectacularAPIView.as_view(), name="schema"),
    *media_urls,
    *defects_urls,
    *ml_models_urls,
    *report_urls,
    # Optional UI:
    path(
        f"{REGULAR_API_PREFIX}docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        f"{REGULAR_API_PREFIX}docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

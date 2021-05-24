"""platon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/

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

import debug_toolbar

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from rest_framework import permissions
from .views import api_root

schema_view = get_schema_view(
    openapi.Info(
        title="PLaTon API",
        default_version='v1',
        description="Documentation of PLaTon apis",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="CeCILL-B"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/v1/admin/', admin.site.urls),

    path('api/v1/', api_root),
    path('api/v1/', include('pl_auth.urls', namespace='pl_auth')),
    path('api/v1/', include('pl_users.urls', namespace='pl_users')),
    path('api/v1/', include('pl_lti.urls', namespace='pl_lti')),
    path('api/v1/', include('pl_sandbox.urls', namespace='pl_sandbox')),

    url(
        r'^api/v1/docs/swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    url(
        r'^api/v1/docs/swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    url(
        r'^api/v1/docs/redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]

if settings.DEBUG:
    urlpatterns += [path('api/v1/__debug__/', include(debug_toolbar.urls))]

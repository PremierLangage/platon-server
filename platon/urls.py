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

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .views import api_root



urlpatterns = [
    path('api/v1/admin/', admin.site.urls),

    path('api/v1/', api_root),
    path('api/v1/', include('pl_auth.urls', namespace='pl_auth')),
    path('api/v1/', include('pl_users.urls', namespace='pl_users')),
    path('api/v1/', include('pl_lti.urls', namespace='pl_lti')),
    path('api/v1/', include('pl_sandbox.urls', namespace='pl_sandbox')),
    path('api/v1/', include('pl_resources.urls', namespace='pl_resources')),
]

if settings.DEBUG and not settings.TESTING:
    import debug_toolbar
    urlpatterns += [path('api/v1/__debug__/', include(debug_toolbar.urls))]

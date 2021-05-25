from django.urls import path, re_path

from . import consumers, views


app_name = 'pl_sandbox'

urlpatterns = [
    path('sandbox/sandboxes/', views.SandboxView.as_view(), name='sandbox-list'),
    path('sandbox/sandboxes/<int:pk>/', views.SandboxView.as_view(), name='sandbox-detail'),

    path('sandbox/sandbox-specs/', views.SandboxSpecsView.as_view(), name='sandbox-specs-list'),
    path('sandbox/sandbox-specs/<int:pk>/', views.SandboxSpecsView.as_view(), name='sandbox-specs-detail'),

    path('sandbox/sandbox-usages/', views.SandboxUsageView.as_view(), name='sandbox-usages-list'),
    path('sandbox/sandbox-usages/<int:pk>/', views.SandboxUsageView.as_view(), name='sandbox-usages-detail'),

    path('sandbox/container-specs/', views.ContainerSpecsView.as_view(), name='container-specs-list'),
    path('sandbox/container-specs/<int:pk>/', views.ContainerSpecsView.as_view(), name='container-specs-detail'),

    path('sandbox/requests/', views.RequestView.as_view(), name='request-list'),
    path('sandbox/requests/<int:pk>/', views.RequestView.as_view(), name='request-detail'),

    path('sandbox/responses/', views.ResponseView.as_view(), name='response-list'),
    path('sandbox/responses/<int:pk>/', views.ResponseView.as_view(), name='response-detail'),

    path('sandbox/command-results/', views.CommandResultView.as_view(), name='command-results-list'),
    path('sandbox/command-results/<int:pk>/', views.CommandResultView.as_view(), name='command-results-detail'),
]

websocket_urlpatterns = [
    re_path(r'ws/sandbox/sandbox-specs/(?P<pk>\d+)/$', consumers.SandboxSpecsConsumer.as_asgi()),
    re_path(r'ws/sandbox/sandbox-usages/(?P<pk>\d+)/$', consumers.SandboxUsageConsumer.as_asgi()),
    re_path(r'ws/sandbox/container-specs/(?P<pk>\d+)/$', consumers.ContainerSpecsConsumer.as_asgi()),
]

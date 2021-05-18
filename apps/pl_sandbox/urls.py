from django.urls import path, re_path

from . import consumers, views


app_name = 'pl_sandbox'

urlpatterns = [
    path('sandboxes/', views.SandboxView.as_view(), name='sandbox-list'),
    path('sandboxes/<int:pk>/', views.SandboxView.as_view(), name='sandbox-detail'),

    path('sandbox-specs/', views.SandboxSpecsView.as_view(), name='sandbox-specs-list'),
    path('sandbox-specs/<int:pk>/', views.SandboxSpecsView.as_view(), name='sandbox-specs-detail'),

    path('sandbox-usages/', views.SandboxUsageView.as_view(), name='sandbox-usages-list'),
    path('sandbox-usages/<int:pk>/', views.SandboxUsageView.as_view(), name='sandbox-usages-detail'),

    path('container-specs/', views.ContainerSpecsView.as_view(), name='container-specs-list'),
    path('container-specs/<int:pk>/', views.ContainerSpecsView.as_view(), name='container-specs-detail'),

    path('requests/', views.RequestView.as_view(), name='request-list'),
    path('requests/<int:pk>/', views.RequestView.as_view(), name='request-detail'),

    path('responses/', views.ResponseView.as_view(), name='response-list'),
    path('responses/<int:pk>/', views.ResponseView.as_view(), name='response-detail'),

    path('command-results/', views.CommandResultView.as_view(), name='command-results-list'),
    path('command-results/<int:pk>/', views.CommandResultView.as_view(), name='command-results-detail'),
]

websocket_urlpatterns = [
    re_path(r'ws/sandbox/sandbox-specs/(?P<pk>\d+)/$', consumers.SandboxSpecsConsumer.as_asgi()),
    re_path(r'ws/sandbox/sandbox-usages/(?P<pk>\d+)/$', consumers.SandboxUsageConsumer.as_asgi()),
    re_path(r'ws/sandbox/container-specs/(?P<pk>\d+)/$', consumers.ContainerSpecsConsumer.as_asgi()),
]

from django.urls import path, re_path

from . import consumers, views


app_name = 'django_sandbox'

urlpatterns = [
    path('sandbox/<int:pk>/', views.SandboxView.as_view(), name='sandbox'),
    path('sandbox/', views.SandboxView.as_view(), name='sandbox_collection'),
    
    path('sandbox_specs/<int:pk>/', views.SandboxSpecsView.as_view(), name='sandbox_specs'),
    path('sandbox_specs/', views.SandboxSpecsView.as_view(), name='sandbox_specs_collection'),
    
    path('container_specs/<int:pk>/', views.ContainerSpecsView.as_view(), name='container_specs'),
    path('container_specs/', views.ContainerSpecsView.as_view(), name='container_specs_collection'),
    
    path('usage/<int:pk>/', views.UsageView.as_view(), name='usage'),
    path('usage/', views.UsageView.as_view(), name='usage_collection'),
    
    path('request/<int:pk>/', views.RequestView.as_view(), name='request'),
    path('request/', views.RequestView.as_view(), name='request_collection'),
    
    path('command_result/<int:pk>/', views.CommandResultView.as_view(), name='command_result'),
    path('command_result/', views.CommandResultView.as_view(), name='command_result_collection'),
    
    path('response/<int:pk>/', views.ResponseView.as_view(), name='response'),
    path('response/', views.ResponseView.as_view(), name='response_collection'),
]

websocket_urlpatterns = [
    re_path(r'ws/sandbox/usage/(?P<pk>\d+)/$', consumers.UsageConsumer.as_asgi()),
    re_path(r'ws/sandbox/sandbox_specs/(?P<pk>\d+)/$', consumers.SandboxSpecsConsumer.as_asgi()),
    re_path(r'ws/sandbox/container_specs/(?P<pk>\d+)/$', consumers.ContainerSpecsConsumer.as_asgi()),
]

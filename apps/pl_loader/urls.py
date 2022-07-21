from django.urls import path
from . import views

app_name = 'pl_loader'

urlpatterns = [
    path(
        'live/resource/<int:resource_id>/',
        views.LoaderView.as_view(),
        name='resource-live'
    )
]

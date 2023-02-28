from django.urls import path
from . import views

app_name = 'pl_loader'

urlpatterns = [
    path(
        'loader/parse/<int:resource_id>/',
        views.testParseView,
        name = 'testParse'
    ),
]

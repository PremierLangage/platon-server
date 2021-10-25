from django.urls import path
from .views import homePageView

app_name = 'pl_runner'

urlpatterns = [
    path('toto', homePageView, name='home')
]
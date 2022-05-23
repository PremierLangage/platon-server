from django.contrib import admin
from .models import Loader

# Register your models here.
@admin.register(Loader)
class LoaderAdmin(admin.ModelAdmin):
    
    list_display = ('pk',)
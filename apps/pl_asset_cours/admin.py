from django.contrib import admin
from .models import AssetCours, AssetCoursSession

# Register your models here.
@admin.register(AssetCours)
class AssetCoursAdmin(admin.ModelAdmin):

    list_display = ('name', 'created_at', 'author', 'content', )


@admin.register(AssetCoursSession)
class AssetCoursSessionAdmin(admin.ModelAdmin):

    list_display = ('asset', 'user', 'data',)
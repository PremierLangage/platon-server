from django.contrib import admin

from .models import Asset, RunnableAsset, RunnableAssetSession
# Register your models here.

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):

    list_display = ('slug_name', 'type', 'author',)


@admin.register(RunnableAsset)
class RunnableAssetAdmin(admin.ModelAdmin):

    list_display = ('asset',)

@admin.register(RunnableAssetSession)
class RunnableAssetSessionAdmin(admin.ModelAdmin):

    list_display = ('asset', 'user', 'session_id',)
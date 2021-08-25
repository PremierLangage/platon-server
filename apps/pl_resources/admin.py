from django.contrib import admin

from .models import Circle, Level, Member, Resource, Topic


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Admin interface for Topic."""

    list_display = ('pk', 'name',)


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    """Admin interface for Level."""

    list_display = ('pk', 'name',)


class MemberInline(admin.TabularInline):
    model = Member


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Admin interface for Circle."""

    list_display = ('pk', 'name',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = (MemberInline,)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    """Admin interface for Resource."""

    list_display = ('pk', 'circle', 'name')
    readonly_fields = ('created_at', 'updated_at')

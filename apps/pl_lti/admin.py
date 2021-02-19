from django.contrib import admin

from pl_lti.models import LMS, LTICourse, LTIUser


@admin.register(LMS)
class LMSAdmin(admin.ModelAdmin):
    """Admin interface for LMS."""
    
    list_display = ('id', 'name', 'url')


@admin.register(LTIUser)
class LTIUserAdmin(admin.ModelAdmin):
    """Admin interface for LTIUser."""
    
    list_display = ('id', 'user', 'lms', 'lms_guid')


@admin.register(LTICourse)
class LTICourseAdmin(admin.ModelAdmin):
    """Admin interface for LTICourse."""
    
    list_display = ('id', 'lms', 'lms_guid')

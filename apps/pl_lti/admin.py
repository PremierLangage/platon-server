from django.contrib import admin

from pl_lti.models import LMS, LTICourse, LTIUser


@admin.register(LMS)
class LMSAdmin(admin.ModelAdmin):
    """Admin interface for LMS."""
    
    list_display = ('guid', 'name', 'url')


@admin.register(LTIUser)
class LTIUserAdmin(admin.ModelAdmin):
    """Admin interface for LTIUser."""
    
    list_display = ('lms_user_id', 'user', 'lms')


@admin.register(LTICourse)
class LTICourseAdmin(admin.ModelAdmin):
    """Admin interface for LTICourse."""
    
    list_display = ('lms_course_id', 'lms')

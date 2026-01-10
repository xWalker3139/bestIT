from django.contrib import admin
from .models import Course, Enrollment, ContactMessage, Lesson

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ('order', 'title', 'video', 'duration', 'is_free')
    ordering = ('order',)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'level', 'duration', 'is_active', 'created_at']
    list_filter = ['level', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']

    inlines = [LessonInline]

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'enrolled_at', 'progress', 'completed']
    list_filter = ['completed', 'enrolled_at', 'course']
    search_fields = ['user__username', 'user__email', 'course__title']
    list_editable = ['progress', 'completed']
    autocomplete_fields = ['user', 'course']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
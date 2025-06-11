from django.contrib import admin
from .models import StudentProfile, Course, Enrollment, Grade, Notification, Attendance

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'date_of_birth', 'created_at')
    search_fields = ('user__username', 'user__email', 'student_id')
    list_filter = ('created_at', 'updated_at')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'instructor', 'credits', 'start_date', 'end_date')
    search_fields = ('code', 'name', 'instructor')
    list_filter = ('start_date', 'end_date', 'credits')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'status')
    search_fields = ('student__user__username', 'course__code', 'course__name')
    list_filter = ('status', 'enrollment_date')

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'graded_date')
    search_fields = ('enrollment__student__user__username', 'enrollment__course__code')
    list_filter = ('graded_date',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'date', 'status')
    search_fields = ('enrollment__student__user__username', 'enrollment__course__code')
    list_filter = ('status', 'date')
    date_hierarchy = 'date'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'created_at')
    search_fields = ('user__username', 'title')
    list_filter = ('is_read', 'created_at')

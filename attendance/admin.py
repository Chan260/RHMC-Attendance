from django.contrib import admin

from .models import (
    Teacher,
    Student,
    Subject,
    Enrollment,
    Attendance
)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'email',
        'user'
    )

    search_fields = (
        'name',
        'email'
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    list_display = (
        'student_id',
        'name',
        'email'
    )

    search_fields = (
        'student_id',
        'name',
        'email'
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        'subject_code',
        'subject_name',
        'teacher'
    )

    search_fields = (
        'subject_code',
        'subject_name'
    )

    list_filter = (
        'teacher',
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'subject',
        'enrollment_date'
    )

    search_fields = (
        'student__student_id',
        'student__name',
        'subject__subject_code',
        'subject__subject_name'
    )

    list_filter = (
        'subject',
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'date',
        'student',
        'subject',
        'status'
    )

    search_fields = (
        'student__student_id',
        'student__name',
        'subject__subject_code',
        'subject__subject_name'
    )

    list_filter = (
        'status',
        'date',
        'subject',
    )
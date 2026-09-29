from django.urls import path
from . import views


urlpatterns = [

    path(
        'teacher/login/',
        views.teacher_login,
        name='teacher_login'
    ),

    path(
        'teacher/dashboard/',
        views.teacher_dashboard,
        name='teacher_dashboard'
    ),

    path(
        'teacher/logout/',
        views.teacher_logout,
        name='teacher_logout'
    ),

    path(
        'teacher/subject/<int:subject_id>/',
        views.subject_students,
        name='subject_students'
    ),

    path(
        'teacher/subject/<int:subject_id>/student/<int:student_id>/attendance/',
        views.mark_attendance,
        name='mark_attendance'
    ),

    path(
        'teacher/attendance-history/',
        views.attendance_history,
        name='attendance_history'
    ),

    path(
        'management/',
        views.management_dashboard,
        name='management_dashboard'
    ),

    path(
    'management/teachers/',
    views.teacher_list,
    name='teacher_list'
    ),

    path(
    'management/teachers/add/',
    views.add_teacher,
    name='add_teacher'
    ),

    path(
    'management/teachers/delete/<int:teacher_id>/',
    views.delete_teacher,
    name='delete_teacher'
    ),

    path(
    'management/students/',
    views.student_list,
    name='student_list'
    ),

    path(
    'management/students/add/',
    views.add_student,
    name='add_student'
    ),

    path(
    'management/students/delete/<int:student_id>/',
    views.delete_student,
    name='delete_student'
    ),

    path(
    'management/subjects/',
    views.subject_list,
    name='subject_list'
    ),

    path(
    'management/subjects/delete/<int:subject_id>/',
    views.delete_subject,
    name='delete_subject'
    ),

    path(
    'management/subjects/add/',
    views.add_subject,
    name='add_subject'
    ),

    path(
    'management/enrollments/add/',
    views.add_enrollment,
    name='add_enrollment'
    ),

    path(
    'management/enrollments/',
    views.enrollment_list,
    name='enrollment_list'
    ),

    path(
    'management/enrollments/delete/<int:enrollment_id>/',
    views.delete_enrollment,
    name='delete_enrollment'
    ),

    path(
    'management/enrollments/edit/<int:enrollment_id>/',
    views.edit_enrollment,
    name='edit_enrollment'
    ),

    path(
    'management/attendance-history/',
    views.management_attendance_history,
    name='management_attendance_history'
    ),

]
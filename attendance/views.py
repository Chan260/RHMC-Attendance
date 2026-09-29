from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count

from .forms import SubjectForm, EnrollmentForm, TeacherForm, StudentForm

from .models import (
    Teacher,
    Student,
    Subject,
    Enrollment,
    Attendance
)


def teacher_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            teacher_exists = Teacher.objects.filter(
                user=user
            ).exists()

            if teacher_exists:

                login(request, user)

                return redirect('teacher_dashboard')

            else:

                return render(
                    request,
                    'teacher_login.html',
                    {
                        'error': 'This account is not registered as a teacher.'
                    }
                )

        else:

            return render(
                request,
                'teacher_login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(request, 'teacher_login.html')


@login_required
def teacher_dashboard(request):

    if request.user.is_superuser:
        return redirect('management_dashboard')

    teacher = get_object_or_404(
        Teacher,
        user=request.user
    )

    subjects = Subject.objects.filter(
        teacher=teacher
    ).annotate(
        student_count=Count(
            'enrollment__student',
            distinct=True
        ) 
    ).order_by(
        'subject_code'
    )

    subject_count = subjects.count()

    student_count = Student.objects.filter(
        enrollment__subject__teacher=teacher
    ).distinct().count()

    today = timezone.localdate()

    present_today = Attendance.objects.filter(
        subject__teacher=teacher,
        date=today,
        status='Present'
    ).count()

    absent_today = Attendance.objects.filter(
        subject__teacher=teacher,
        date=today,
        status='Absent'
    ).count()

    recent_attendance = Attendance.objects.filter(
        subject__teacher=teacher
    ).select_related(
        'student',
        'subject'
    ).order_by(
        '-date',
        '-id'
    )[:5]

    context = {
        'teacher': teacher,
        'subjects': subjects,
        'subject_count': subject_count,
        'student_count': student_count,
        'present_today': present_today,
        'absent_today': absent_today,
        'recent_attendance': recent_attendance,
    }

    return render(
        request,
        'teacher_dashboard.html',
        context
    )


def teacher_logout(request):

    logout(request)

    return redirect('teacher_login')



@login_required
def subject_students(request, subject_id):

    teacher = Teacher.objects.get(
        user=request.user
    )

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        teacher=teacher
    )

    enrollments = Enrollment.objects.filter(
        subject=subject
    ).select_related('student')

    today = timezone.localdate()

    attendance_records = Attendance.objects.filter(
        subject=subject,
        date=today
    ).select_related('student')

    for enrollment in enrollments:

        enrollment.attendance_status = None

        for attendance in attendance_records:

            if attendance.student_id == enrollment.student_id:

                enrollment.attendance_status = attendance.status

                break

    context = {
        'teacher': teacher,
        'subject': subject,
        'enrollments': enrollments,
    }

    return render(
        request,
        'subject_students.html',
        context
    )


@login_required
def mark_attendance(request, subject_id, student_id):

    teacher = Teacher.objects.get(
        user=request.user
    )

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        teacher=teacher
    )

    enrollment = get_object_or_404(
        Enrollment,
        subject=subject,
        student_id=student_id
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        if status in ['Present', 'Absent']:

            Attendance.objects.update_or_create(
                student=enrollment.student,
                subject=subject,
                date=timezone.localdate(),
                defaults={
                    'status': status
                }
            )

    return redirect(
        'subject_students',
        subject_id=subject.id
    )


@login_required
def attendance_history(request):

    teacher = Teacher.objects.get(
        user=request.user
    )

    attendance_records = Attendance.objects.filter(
        subject__teacher=teacher
    ).select_related(
        'student',
        'subject'
    )

    selected_date = request.GET.get('date')
    selected_subject = request.GET.get('subject')
    selected_status = request.GET.get('status')

    if selected_date:
        attendance_records = attendance_records.filter(
            date=selected_date
        )

    if selected_subject:
        attendance_records = attendance_records.filter(
            subject_id=selected_subject
        )

    if selected_status:
        attendance_records = attendance_records.filter(
            status=selected_status
        )

    attendance_records = attendance_records.order_by(
        '-date'
    )

    subjects = teacher.subject_set.all().order_by(
        'subject_code'
    )

    context = {
        'teacher': teacher,
        'attendance_records': attendance_records,
        'selected_date': selected_date,
        'selected_subject': selected_subject,
        'selected_status': selected_status,
        'subjects': subjects,
    }

    return render(
        request,
        'attendance_history.html',
        context
    )

@login_required
def teacher_list(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    teachers = Teacher.objects.all().order_by('name')

    context = {
        'teachers': teachers,
    }

    return render(
        request,
        'teacher_list.html',
        context
    )

@login_required
def student_list(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    students = Student.objects.all().order_by('student_id')

    context = {
        'students': students,
    }

    return render(
        request,
        'student_list.html',
        context
    )

@login_required
def management_dashboard(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    teacher_count = Teacher.objects.count()

    student_count = Student.objects.count()

    subject_count = Subject.objects.count()

    enrollment_count = Enrollment.objects.count()

    present_count = Attendance.objects.filter(
        status='Present'
    ).count()

    absent_count = Attendance.objects.filter(
        status='Absent'
    ).count()

    attendance_count = Attendance.objects.count()

    recent_attendance = Attendance.objects.select_related(
        'student',
        'subject'
    ).order_by(
        '-date'
    )[:5]

    context = {
    'teacher_count': teacher_count,
    'student_count': student_count,
    'subject_count': subject_count,
    'enrollment_count': enrollment_count,
    'present_count': present_count,
    'absent_count': absent_count,
    'attendance_count': attendance_count,
    'recent_attendance': recent_attendance,
    }

    return render(
        request,
        'management_dashboard.html',
        context
    )

@login_required
def add_teacher(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    if request.method == 'POST':

        form = TeacherForm(request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():

                form.add_error(
                    'username',
                    'This username is already in use.'
                )

            else:

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )

                Teacher.objects.create(
                    user=user,
                    name=name,
                    email=email
                )

                return redirect('teacher_list')

    else:

        form = TeacherForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'add_teacher.html',
        context
    )

@login_required
def add_subject(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    if request.method == 'POST':

        form = SubjectForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('subject_list')

    else:

        form = SubjectForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'add_subject.html',
        context
    )

@login_required
def add_enrollment(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    if request.method == 'POST':

        form = EnrollmentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('enrollment_list')

    else:

        form = EnrollmentForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'add_enrollment.html',
        context
    )

@login_required
def enrollment_list(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    enrollments = Enrollment.objects.all().select_related(
        'student',
        'subject',
        'subject__teacher'
    ).order_by(
        'subject__subject_code',
        'student__student_id'
    )

    context = {
        'enrollments': enrollments,
    }

    return render(
        request,
        'enrollment_list.html',
        context
    )

@login_required
def delete_enrollment(request, enrollment_id):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id
    )

    if request.method == 'POST':

        enrollment.delete()

        return redirect('enrollment_list')

    context = {
        'enrollment': enrollment,
    }

    return render(
        request,
        'delete_enrollment.html',
        context
    )

@login_required
def edit_enrollment(request, enrollment_id):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id
    )

    if request.method == 'POST':

        form = EnrollmentForm(
            request.POST,
            instance=enrollment
        )

        if form.is_valid():

            form.save()

            return redirect('enrollment_list')

    else:

        form = EnrollmentForm(
            instance=enrollment
        )

    context = {
        'form': form,
        'enrollment': enrollment,
    }

    return render(
        request,
        'edit_enrollment.html',
        context
    )

@login_required
def subject_list(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    subjects = Subject.objects.all().select_related(
        'teacher'
    ).order_by('subject_code')

    context = {
        'subjects': subjects,
    }

    return render(
        request,
        'subject_list.html',
        context
    )

@login_required
def management_attendance_history(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    attendance_records = Attendance.objects.all().select_related(
        'student',
        'subject',
        'subject__teacher'
    ).order_by('-date')

    selected_date = request.GET.get('date')
    selected_subject = request.GET.get('subject')
    selected_status = request.GET.get('status')

    if selected_date:
        attendance_records = attendance_records.filter(
            date=selected_date
        )

    if selected_subject:
        attendance_records = attendance_records.filter(
            subject_id=selected_subject
        )

    if selected_status:
        attendance_records = attendance_records.filter(
            status=selected_status
        )

    subjects = Subject.objects.all().order_by('subject_code')

    context = {
        'attendance_records': attendance_records,
        'subjects': subjects,
        'selected_date': selected_date,
        'selected_subject': selected_subject,
        'selected_status': selected_status,
    }

    return render(
        request,
        'management_attendance_history.html',
        context
    )

@login_required
def delete_teacher(request, teacher_id):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    teacher = get_object_or_404(
        Teacher,
        id=teacher_id
    )

    if request.method == 'POST':

        if teacher.user:
            teacher.user.delete()

        else:
            teacher.delete()

        return redirect('teacher_list')

    context = {
        'teacher': teacher,
    }

    return render(
        request,
        'delete_teacher.html',
        context
    )

@login_required
def add_student(request):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    if request.method == 'POST':

        form = StudentForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('student_list')

    else:

        form = StudentForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'add_student.html',
        context
    )

@login_required
def delete_student(request, student_id):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == 'POST':

        student.delete()

        return redirect('student_list')

    context = {
        'student': student,
    }

    return render(
        request,
        'delete_student.html',
        context
    )

@login_required
def delete_subject(request, subject_id):

    if not request.user.is_superuser:
        return redirect('teacher_dashboard')

    subject = get_object_or_404(
        Subject,
        id=subject_id
    )

    if request.method == 'POST':

        subject.delete()

        return redirect('subject_list')

    context = {
        'subject': subject,
    }

    return render(
        request,
        'delete_subject.html',
        context
    )
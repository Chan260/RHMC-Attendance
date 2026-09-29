from django import forms

from .models import Subject, Enrollment, Teacher, Student


class SubjectForm(forms.ModelForm):

    class Meta:

        model = Subject

        fields = [
            'subject_code',
            'subject_name',
            'teacher'
        ]

        labels = {
            'subject_code': 'Subject Code',
            'subject_name': 'Subject Name',
            'teacher': 'Assigned Teacher'
        }


class EnrollmentForm(forms.ModelForm):

    class Meta:

        model = Enrollment

        fields = [
            'student',
            'subject'
        ]

        labels = {
            'student': 'Student',
            'subject': 'Subject'
        }

class TeacherForm(forms.ModelForm):

    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter username'
            }
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter password'
            }
        )
    )

    class Meta:

        model = Teacher

        fields = [
            'name',
            'email'
        ]

        labels = {
            'name': 'Teacher Name',
            'email': 'Email Address'
        }

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter teacher name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter teacher email'
                }
            )
        }

class StudentForm(forms.ModelForm):

    class Meta:

        model = Student

        fields = [
            'student_id',
            'name',
            'email'
        ]

        labels = {
            'student_id': 'Student ID',
            'name': 'Student Name',
            'email': 'Email Address'
        }

        widgets = {
            'student_id': forms.TextInput(
                attrs={
                    'placeholder': 'Enter student ID'
                }
            ),

            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter student name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter student email'
                }
            )
        }
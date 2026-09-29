from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(
        'auth.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    subject_code = models.CharField(max_length=20, unique=True)
    subject_name = models.CharField(max_length=100)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.subject_name


class Enrollment(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject'],
                name='unique_student_subject'
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.subject.subject_name}"


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['student', 'subject', 'date'],
                name='unique_student_subject_date'
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
# Create your models here.

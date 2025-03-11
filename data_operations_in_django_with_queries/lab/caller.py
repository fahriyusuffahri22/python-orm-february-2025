import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import F, Value
from django.db.models.functions import Replace
from main_app.models import Student


def add_students():
    Student.objects.bulk_create([
        Student(
            student_id='FC5204',
            first_name='John',
            last_name='Doe',
            birth_date='1995-05-15',
            email='john.doe@university.com'
        ),
        Student(
            student_id='FE0054',
            first_name='Jane',
            last_name='Smith',
            email='jane.smith@university.com'
        ),
        Student(
            student_id='FH2014',
            first_name='Alice',
            last_name='Johnson',
            birth_date='1998-02-10',
            email='alice.johnson@university.com'
        ),
        Student(
            student_id='FH2015',
            first_name='Bob',
            last_name='Wilson',
            birth_date='1996-11-25',
            email='bob.wilson@university.com'
        )
    ])


def get_students_info():
    return '\n'.join(
        f'Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}'
        for student in Student.objects.all()
    )


def update_students_emails():
    Student.objects.filter(email__endswith='university.com').update(
        email=Replace(F('email'), Value('university.com'), Value('uni-students.com'))
    )


def truncate_students():
    Student.objects.all().delete()

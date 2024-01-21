import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from backend.models import Attendance, Course, Mentor, Section, Student, User


@pytest.fixture
def setup_section(db):
    mentor_user = User.objects.create(
        username="demo_mentor",
        first_name="Demo",
        last_name="Mentor",
        email="demo_mentor@berkeley.edu",
    )
    course = Course.objects.create(name="CS70")
    mentor = Mentor.objects.create(user=mentor_user, course=course)
    section = Section.objects.create(
        mentor=mentor, capacity=5, description="description"
    )

    student1_user = User.objects.create(
        username="demo_student", first_name="Demo", last_name="Student"
    )
    student1 = Student.objects.create(
        user=student1_user, course=course, section=section, active=True, banned=False
    )
    Attendance.objects.create(
        student=student1, date=datetime.date(2022, 1, 1), presence=""
    )
    Attendance.objects.create(
        student=student1, date=datetime.date(2022, 2, 2), presence=""
    )
    Attendance.objects.create(
        student=student1, date=datetime.date(2022, 3, 3), presence=""
    )

    student2_user = User.objects.create(
        username="other_student", first_name="Other", last_name="Student"
    )
    student2 = Student.objects.create(
        user=student2_user, course=course, section=section, active=True, banned=False
    )
    Attendance.objects.create(
        student=student2, date=datetime.date(2022, 1, 10), presence=""
    )
    Attendance.objects.create(
        student=student2, date=datetime.date(2022, 2, 20), presence=""
    )
    Attendance.objects.create(
        student=student2, date=datetime.date(2022, 3, 30), presence=""
    )

    return student1, student2, mentor, section, course


@pytest.mark.django_db
def test_get_student_attendances(client, setup_section):
    """
    Ensure that the student attendances are retrieved correctly
    """
    student1, student2, _mentor, section, _course = setup_section

    student1_attendances_url = reverse(
        "student-attendances", kwargs={"student_id": student1.id}
    )
    student1_response = client.get(student1_attendances_url)
    student1_data = student1_response.json()

    student2_attendances_url = reverse(
        "student-attendances", kwargs={"student_id": student2.id}
    )
    student2_response = client.get(student2_attendances_url)
    student2_data = student2_response.json()

    assert student1_response.status_code == status.HTTP_200_OK
    assert student2_response.status_code == status.HTTP_200_OK
    # should have 3 attendances each
    assert len(student1_data) == 3
    assert len(student2_data) == 3

    # student1_data should be associated with student 1
    for attendance in student1_data:
        assert attendance["student"]["id"] == student1.id
        assert attendance["student"]["user"]["id"] == student1.user.id
        assert attendance["student"]["section"]["id"] == section.id

    # student2_data should be associated with student 2
    for attendance in student2_data:
        assert attendance["student"]["id"] == student2.id
        assert attendance["student"]["user"]["id"] == student2.user.id
        assert attendance["student"]["section"]["id"] == section.id


@pytest.mark.django_db
def test_update_student_attendance(client, setup_section):
    """
    Ensure that one can update a student's attendance
    """
    student1, _student2, _mentor, _section, _course = setup_section

    student1_attendance = Attendance.objects.filter(student=student1).first()

    student1_attendances_url = reverse(
        "student-attendances", kwargs={"student_id": student1.id}
    )
    response = client.put(
        student1_attendances_url,
        data={"id": student1_attendance.id, "presence": "PR"},
        content_type="application/json",
    )
    assert response.status_code == status.HTTP_202_ACCEPTED

    student1_attendance.refresh_from_db()
    assert student1_attendance.presence == "PR"

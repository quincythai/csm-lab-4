import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from backend.models import Course, Mentor, Section, Student, User


@pytest.fixture()
def setup_section(db):
    """
    Set up a section.
    """

    course = Course.objects.create(name="CS70")

    mentor_user = User.objects.create(
        username="demo_mentor",
        first_name="Demo",
        last_name="Mentor",
        email="demo_mentor@berkeley.edu",
    )
    mentor = Mentor.objects.create(user=mentor_user, course=course)
    section = Section.objects.create(
        mentor=mentor, capacity=5, description="description"
    )
    student1_user = User.objects.create(
        username="demo_student",
        first_name="Demo",
        last_name="Student",
        email="demo_student@berkeley.edu",
    )
    student1 = Student.objects.create(
        user=student1_user, course=course, section=section, active=True, banned=False
    )
    student2_user = User.objects.create(
        username="other_student",
        first_name="Other",
        last_name="Student",
        email="other_student@berkeley.edu",
    )
    student2 = Student.objects.create(
        user=student2_user, course=course, section=section, active=True, banned=False
    )

    return student1, student2, mentor, section, course


@pytest.mark.django_db
def test_drop_student(client, setup_section):
    """
    Ensure that a student can be dropped from the section.
    """

    student1, student2, _mentor, _section, _course = setup_section

    drop_url = reverse("student-drop", kwargs={"student_id": student1.id})
    response = client.patch(drop_url)
    assert response.status_code == status.HTTP_202_ACCEPTED

    # student 1 should now be inactive
    student1.refresh_from_db()
    assert student1.active is False

    # student 2 should not be changed
    student2.refresh_from_db()
    assert student2.active is True

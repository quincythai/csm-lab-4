from django.urls import path

from . import views

urlpatterns = [
    path("users/", views.users, name="users"),
    path("sections/", views.sections, name="sections"),
    path(
        "sections/<int:section_id>/students/",
        views.section_students,
        name="section-students",
    ),
    path(
        "sections/<int:section_id>/details/",
        views.section_details,
        name="section-details",
    ),
    path(
        "students/<int:student_id>/details/",
        views.student_details,
        name="student-details",
    ),
    path(
        "students/<int:student_id>/attendances/",
        views.student_attendances,
        name="student-attendances",
    ),
    path("students/<int:student_id>/drop/", views.student_drop, name="student-drop"),
]

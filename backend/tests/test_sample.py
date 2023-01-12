"""
You should structure your tests similarly to what is in this file.

Feel free to make one test file per view, and give each file an intuitive name,
or put all the tests in one file---regardless of which organizational structure you choose,
try to keep the files decently short and readable though.

In the real repository, we'd combine the tests for similar views together,
but since this is just practice, you may choose to organize in any way you wish.
"""

import pytest
from django.urls import reverse
from rest_framework import status

from backend.models import User


@pytest.fixture  # mark this function as a fixture, providing data to a test
def setup_section(db):  # the `db` argument tells pytest to set up the test database
    """
    Set up a student, mentor, section, and a course.

    This can be reused throughout various tests with the same initial data.
    """

    # create your objects here to set up all of the data
    User.objects.create(
        username="demo_user",
        first_name="Demo",
        last_name="User",
        email="demo_user@berkeley.edu",
    )

    # this just keeps python from complaining
    student = None
    mentor = None
    section = None
    course = None

    # return the data you've setup;
    # this isn't strictly necessary, especially since you can also query the database directly,
    # but it can make tests cleaner
    return student, mentor, section, course


@pytest.mark.django_db  # mark this function as a test that uses the django database
def test_section_is_set_up(client, setup_section):
    """
    Ensure that the section has been set up correctly.

    A lot of this test does not actually test anything; it's mainly for demonstration purposes
    for the various methods you can use, and to give a general structure of a test.
    """
    # When we specify `setup_section` as an argument to this test,
    # pytest will run the `setup_section` fixture, and the value of the
    # argument is the return value of the fixture.
    # This means that we can simply unpack the `setup_section` argument
    # to get the objects we created earlier.
    student, mentor, section, course = setup_section

    # You can also make any other queries here to retrieve things from the database
    user = User.objects.get(username="demo_user")

    # To get the URL for the request, you can use the `reverse` method from Django.
    # When registering your urls in `urls.py`, you can give a `name=` keyword argument
    # so that you can reference the view easily elsewhere in the backend.
    request_url = reverse("users")

    # If you want to mock a request sent by the frontend, you can use the `client` fixture
    # (provided by pytest-django, given to this test with the `client` argument).
    # See the documentation for the Django client for methods and fields on the response object:
    # https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.Client
    # https://docs.djangoproject.com/en/4.1/topics/testing/tools/#django.test.Response
    response = client.get(request_url)
    # When making a PUT or POST request with data, you'd do something like the following:
    #
    #   response = client.put(request_url, data={...}, content_type="application/json")
    #
    # The `content_type` is important here, since by default the content type is
    # `multipart/form-data`, which is not normally accepted.

    # This should return something like [{"id": ..., "username": ..., ...}]
    data = response.json()

    # Now, you can make a bunch of assertions to check that the action was performed correctly

    # If you expect the request to modify the models, make sure you refresh them from the database;
    # otherwise, the python object will still have the previous values.
    user.refresh_from_db()

    assert user.username == "demo_user"

    # ensure the request went through successfully
    assert response.status_code == status.HTTP_200_OK
    # ensure there is only one user
    assert len(data) == 1
    # ensure returned data matches expected from database
    user_response = data[0]
    assert user_response["username"] == "demo_user"
    assert user_response["email"] == "demo_user@berkeley.edu"
    assert user_response["first_name"] == "Demo"
    assert user_response["last_name"] == "User"

    # this is just here so that the variables aren't actually unused
    assert student is None
    assert mentor is None
    assert section is None
    assert course is None

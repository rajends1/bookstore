"""Test Views for bookstore user accounts."""

import pytest
from django.contrib.auth import get_user_model
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ..forms import CustomUserChangeForm
from ..models import CustomUser
from ..views import UserRedirectView, UserUpdateView

pytestmark = pytest.mark.django_db


class TestUserSignup(TestCase):
    username = "newuser"
    email = "newuser@example.com"

    def setUp(self):
        url = reverse("account_signup")
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertContains(self.response, "Sign Up")
        self.assertNotContains(self.response, "This does not belong here.")

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(  # noqa: F841
            self.username, self.email
        )
        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()[0].username, self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)


class TestUserUpdateView:
    """TODO:

    extracting view initialization code as class-scoped fixture
    would be great if only pytest-django supported non-function-scoped
    fixture db access -- this is a work-in-progress for now:
    https://github.com/pytest-dev/pytest-django/pull/258
    """

    def dummy_get_response(self, request: HttpRequest):
        return None

    def test_get_success_url(self, user: CustomUser, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == f"/accounts/{user.username}/"

    def test_get_object(self, user: CustomUser, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_form_valid(self, user: CustomUser, request_factory: RequestFactory):
        view = UserUpdateView()
        form_data = {"name": "John Doe"}
        request = request_factory.post(reverse("user_update"), form_data)

        # Add the session/message middleware to the request
        SessionMiddleware(self.dummy_get_response).process_request(request)
        MessageMiddleware(self.dummy_get_response).process_request(request)
        request.user = user

        view.request = request

        # Initialize the form
        form = CustomUserChangeForm()
        form.cleaned_data = {}
        view.form_valid(form)

        response = UserUpdateView.as_view()(request)
        user.refresh_from_db()

        assert response.status_code == 302
        assert user.name == form_data["name"]


class TestUserRedirectView:
    def test_get_redirect_url(self, user: CustomUser, request_factory: RequestFactory):
        view = UserRedirectView()
        request = request_factory.get("/fake-url")
        request.user = user

        view.request = request

        assert view.get_redirect_url() == f"/accounts/{user.username}/"

from unittest.mock import patch

from django.core.exceptions import MultipleObjectsReturned
from django.test import SimpleTestCase
from django.urls import reverse

from project.social_adapters import CustomSocialAccountAdapter


class GoogleLoginPageTests(SimpleTestCase):
    def test_login_page_contains_google_login_link(self):
        response = self.client.get(reverse("users:login"))
        self.assertContains(response, "google_login")


class GoogleSocialLoginTests(SimpleTestCase):
    def test_get_user_by_email_returns_first_match_when_duplicates_exist(self):
        adapter = CustomSocialAccountAdapter()
        expected_user = type("User", (), {"email": "duplicate@gmail.com"})()

        class DummyQuerySet:
            def __init__(self, value):
                self.value = value

            def order_by(self, *args):
                return self

            def first(self):
                return self.value

        class DummyUserModel:
            class DoesNotExist(Exception):
                pass

            class objects:
                @staticmethod
                def get(**kwargs):
                    raise MultipleObjectsReturned("duplicate")

                @staticmethod
                def filter(**kwargs):
                    return DummyQuerySet(expected_user)

        class DummyEmailAddress:
            def __init__(self, email, verified):
                self.email = email
                self.verified = verified

        class DummySocialLogin:
            def __init__(self):
                self.email_addresses = [DummyEmailAddress("duplicate@gmail.com", True)]
                self.provider = type("Provider", (), {"app": None, "get_settings": lambda self: {}})()

        with patch("project.social_adapters.filter_users_by_email", return_value=[expected_user]):
            result = adapter.authenticate_by_email(DummySocialLogin())

        self.assertIs(result[0], expected_user)

    def test_pre_social_login_does_not_raise_when_email_lookup_returns_multiple_matches(self):
        adapter = CustomSocialAccountAdapter()
        expected_user = type("User", (), {"email": "duplicate@gmail.com"})()

        class DummySocialLogin:
            def __init__(self):
                self.user = type("User", (), {"email": "duplicate@gmail.com"})()
                self.connected_user = None

            def connect(self, request, user):
                self.connected_user = user

        social_login = DummySocialLogin()

        with patch("project.social_adapters.filter_users_by_email", side_effect=MultipleObjectsReturned("duplicate")):
            adapter.pre_social_login(object(), social_login)

        self.assertIsNone(social_login.connected_user)

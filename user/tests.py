from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class UserTests(APITestCase):
    def setUp(self):
        self.create_url = reverse("user:register")
        self.me_url = reverse("user:profile")

        self.user_data = {
            "email": "test@test.com",
            "password": "testpassword123",
        }

    def test_create_user(self):
        res = self.client.post(self.create_url, self.user_data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(get_user_model().objects.get().email, "test@test.com")

    def test_me_page_requires_auth(self):
        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_page_works_for_auth_user(self):
        user = get_user_model().objects.create_user(**self.user_data)
        self.client.force_authenticate(user=user)

        res = self.client.get(self.me_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], user.email)
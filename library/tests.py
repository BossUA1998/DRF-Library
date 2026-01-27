from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from library.models import Book


class BookTests(APITestCase):
    def setUp(self):
        self.book_url = reverse("library:book-list")
        self.sample_book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=1.50
        )

        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="password123"
        )
        self.admin = get_user_model().objects.create_superuser(
            email="admin@test.com", password="password123"
        )

    def test_list_books_public(self):
        res = self.client.get(self.book_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_book_forbidden_for_user(self):
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "New Book",
            "author": "Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 2.00
        }
        res = self.client.post(self.book_url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_allowed_for_admin(self):
        self.client.force_authenticate(user=self.admin)
        payload = {
            "title": "Admin Book",
            "author": "Admin Author",
            "cover": "SOFT",
            "inventory": 5,
            "daily_fee": 10.50
        }
        res = self.client.post(self.book_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
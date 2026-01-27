import datetime
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from library.models import Book
from borrowings.models import Borrowing

class BorrowingTests(APITestCase):
    def setUp(self):
        self.borrowing_url = reverse("borrowings:borrowing-list")
        self.user = get_user_model().objects.create_user(
            email="user@test.com", password="password123"
        )
        self.book = Book.objects.create(
            title="Python Book",
            author="Guido",
            cover="HARD",
            inventory=5,
            daily_fee=0.50
        )
        self.client.force_authenticate(user=self.user)

    def test_list_borrowings(self):
        Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7)
        )

        res = self.client.get(self.borrowing_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

    def test_create_borrowing_success(self):
        payload = {
            "book": self.book.id,
            "expected_return_date": (datetime.date.today() + datetime.timedelta(days=5)).isoformat()
        }

        res = self.client.post(self.borrowing_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 4)

    def test_create_borrowing_no_inventory(self):
        self.book.inventory = 0
        self.book.save()

        payload = {
            "book": self.book.id,
            "expected_return_date": "2026-01-01"
        }
        res = self.client.post(self.borrowing_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
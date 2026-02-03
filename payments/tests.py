import datetime
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from library.models import Book
from borrowings.models import Borrowing
from payments.models import Payment


class PaymentTests(APITestCase):
    def setUp(self):
        self.payment_list_url = reverse("payments:payment-list")

        self.user = get_user_model().objects.create_user(
            email="user@test.com",
            password="testpassword123"
        )
        self.client.force_authenticate(self.user)

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=Decimal("1.50")
        )

        self.borrowing = Borrowing.objects.create(
            user=self.user,
            book=self.book,
            expected_return_date=datetime.date.today() + datetime.timedelta(days=7)
        )

        self.payment = Payment.objects.create(
            status="PENDING",
            type="PAYMENT",
            borrowing=self.borrowing,
            money_to_pay=Decimal("10.50"),
            session_url="http://example.com/session",
            session_id="sess_12345"
        )

    def test_list_payments(self):
        res = self.client.get(self.payment_list_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["id"], self.payment.id)

    def test_retrieve_payment_detail(self):
        url = reverse("payments:payment-detail", args=[self.payment.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["session_id"], "sess_12345")
        self.assertEqual(res.data["money_to_pay"], "10.50")

    def test_payments_list_requires_auth(self):
        self.client.logout()
        res = self.client.get(self.payment_list_url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
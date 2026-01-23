from rest_framework import viewsets

from library.permissions import IsAdminOrReadOnly
from library.models import Book
from library.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

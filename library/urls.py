from django.urls import path
from rest_framework.routers import DefaultRouter

from library.views import BookViewSet

router = DefaultRouter()
router.register("", BookViewSet)

urlpatterns = router.urls

app_name = "library"
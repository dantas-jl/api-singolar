from .post import post_router
from django.urls import path, include

urlpatterns = [
    path("", include(post_router.urls)),
]
from .post import post_router
from .comment import comment_router
from django.urls import path, include

urlpatterns = [
    path("", include(post_router.urls)),
    path("", include(comment_router.urls)),
]
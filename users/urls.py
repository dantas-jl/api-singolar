from django.urls import path, include
from rest_framework import routers
from users.views import CustomUserViewSet

router_users = routers.SimpleRouter()
router_users.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router_users.urls)),
]

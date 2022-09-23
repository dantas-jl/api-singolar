from django.urls import path, include
from rest_framework import routers
from users.views import CustomUserViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router_users = routers.SimpleRouter()
router_users.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router_users.urls)),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
]

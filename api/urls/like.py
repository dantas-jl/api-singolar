from rest_framework.routers import DefaultRouter
from api.views.like import LikeViewSet

like_router = DefaultRouter()
like_router.register("likes", LikeViewSet, basename="likes")
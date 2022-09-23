from rest_framework.routers import DefaultRouter
from api.views.post import PostViewSet

post_router = DefaultRouter()
post_router.register("posts", PostViewSet, basename="post")
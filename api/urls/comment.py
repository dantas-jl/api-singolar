from rest_framework.routers import DefaultRouter
from api.views.comment import CommentViewSet

comment_router = DefaultRouter()
comment_router.register("comments", CommentViewSet, basename="comments")
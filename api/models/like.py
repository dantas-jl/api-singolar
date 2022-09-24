from django.db import models
from api.models.comment import Comment

class Like(models.Model):

    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="likes"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "like"
        unique_together = ("author", "comment")
        verbose_name = "Like"
        verbose_name_plural = "Likes"
        ordering = ["-created_at"]
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="posts"
    )
    content = models.CharField(max_length=140)
    picture = models.ImageField(upload_to="post_pictures", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post"
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]
    
    def delete(self, *args, **kwargs):
        
        if self.picture:
            self.picture.delete()
        super().delete(*args, **kwargs)
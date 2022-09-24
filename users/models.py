from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=200, blank=True)
    birth = models.DateField()
    picture = models.ImageField(
        upload_to="user_pictures",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        blank=True,
        null=True,
    )
    email = models.EmailField(max_length=50, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ["name", "birth", "email"]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def delete(self, *args, **kwargs):
        
        if self.picture:
            self.picture.delete()
        super().delete(*args, **kwargs)
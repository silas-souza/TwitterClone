from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage


class User(AbstractUser):
    profile_picture = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    following = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="followers",
        blank=True,
    )